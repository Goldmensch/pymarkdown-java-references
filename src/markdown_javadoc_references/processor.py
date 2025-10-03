import logging
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as etree

from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import InlineProcessor

from .docsite import docsite
from .reference import create_or_none
from .reference import Type

from .reference import raw_pattern as ref_pattern

logger = logging.getLogger(__name__)


def process_url(url):
    stripped_url = url.removesuffix('/')
    return docsite.load(stripped_url)


def match(klasses, reference):
    # search in each class
    for klass in klasses:
        # compare package if given
        if reference.package is not None and (klass.package != reference.package): continue
        # compare method if given
        if reference.member_name is not None:
            if reference.type == Type.METHOD:
                # get all methods for class
                methods = klass.methods
                # search in each member
                for method in methods:
                    # compare method name
                    if reference.member_name != method.name: continue
                    # compare parameter size
                    if len(reference.parameters) != len(method.parameters): continue

                    # compare parameters
                    parameter_match = True
                    for r_p, m_p in zip(reference.parameters, method.parameters):
                        if not m_p.endswith(r_p): parameter_match = False
                    if not parameter_match: continue

                    return method.url
            else:
                # get all fields
                fields = klass.fields

                # compare each field
                for field in fields:
                    if reference.member_name != field.name: continue
                    return field.url

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
            klasses = site.klasses_for_ref(reference)
            link = match(klasses, reference)
            if link is not None: matches.append(link)
        return matches


auto_link_pattern = rf'<({ref_pattern[:-1]})>$'
class AutoLinkJavaDocProcessor(InlineProcessor):
    def __init__(self, md):
        super().__init__(auto_link_pattern, md)

    def handleMatch(self, m, data):
        text = m.group(1)
        el = etree.Element('a')
        el.set('href', text)
        el.text = text
        return el, m.start(0), m.end(0)