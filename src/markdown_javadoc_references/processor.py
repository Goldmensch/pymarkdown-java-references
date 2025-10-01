import logging
from concurrent.futures import ThreadPoolExecutor

from markdown.treeprocessors import Treeprocessor

from .docsite import docsite
from .reference import create_or_none

logger = logging.getLogger(__name__)


def process_url(url):
    stripped_url = url.removesuffix('/')
    return docsite.load(stripped_url)


def match(site_classes, reference):
    if reference.class_name not in site_classes: return None

    # search in each class
    for klass in site_classes[reference.class_name]:
        # compare package if given
        if reference.package is not None and (klass.package != reference.package): continue
        # compare method if given
        if reference.method_name is not None:
            # get all methods for class
            methods = klass.methods
            # search in each member
            for method in methods:
                # compare method name
                if reference.method_name != method.name: continue
                # compare parameter size
                if len(reference.parameters) != len(method.parameters): continue

                # compare parameters
                parameter_match = True
                for r_p, m_p in zip(reference.parameters, method.parameters):
                    if not m_p.endswith(r_p): parameter_match = False
                if not parameter_match: continue

                return method.url

        else:  # if not given, just reference found class
            return klass.url

    return None


class JavaDocProcessor(Treeprocessor):
    def __init__(self, md, urls):
        super().__init__(md)

        self.sites = list()

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(process_url, urls))
            self.sites.extend(results)

    def run(self, root):
        for el in root.iter('a'):
            href = el.get('href', '')
            reference = create_or_none(href)
            if reference is not None:
                links = self.find_matching_javadoc(reference)

                if len(links) == 0:
                    logger.warning(f'No javadoc matching {href} was found!')
                    el.text = f'Invalid reference to {href}'
                elif len(links) > 1:
                    logger.warning(
                        f'Multiple javadoc matching {href} found! Please be more specific, maybe add a pacakge? Found javadocs: {'; '.join(links)}')
                    el.text = f'Invalid reference to {href}'
                else:
                    url = links[0]
                    el.set('href', url)

    def find_matching_javadoc(self, reference):
        matches = list()
        for site in self.sites:
            link = match(site, reference)
            if link is not None: matches.append(link)
        return matches
