from .docsite import docsite
from .reference import create_or_none
from .reference import Type
from .entities import Entity

import xml.etree.ElementTree as etree

from .util import get_logger

logger = get_logger(__name__)


def matches(klasses, reference):
    links = dict()

    # search in each class
    for klass in klasses:
        joined_klass = klass.package + '.' + klass.name

        # if package is given -> compare package + class. Subclasses in references are treated as package
        if reference.package is not None:
            joined_reference = reference.package + '.' + reference.class_name
            if not joined_klass.endswith(joined_reference): continue
        elif not joined_klass.endswith(reference.class_name):
            continue

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

                    links[method.url] = method
            else:
                # get all fields
                fields = klass.fields

                # compare each field
                for field in fields:
                    if reference.member_name != field.name: continue
                    links[field.url] = field

        else:  # if not given, just reference found class
            links[klass.url] = klass

    return links


def process_url(url):
    logger.debug(f"Process url {url}")

    stripped_url = url.removesuffix('/')
    return docsite.load(stripped_url)


class Resolver:
    def __init__(self, urls):
        self.sites = dict()

        for entry in urls:
            if isinstance(entry, str):
                site = process_url(entry)
                if site is None: continue
                self.sites[entry.strip()] = site
            elif isinstance(entry, dict) and 'alias' in entry and 'url' in entry:
                site = process_url(entry['url'])
                if site is None: continue
                self.sites[entry['alias'].strip()] = site
            else:
                raise TypeError(
                    f"Invalid entry in urls config: {entry!r}. "
                    f"Expected string or dict with 'alias' and 'url'."
                )

    def resolve(self, text: str, ref: str) -> tuple[Entity | None, etree.Element]:
        logger.debug(f"Resolving link with text {text} and reference {ref}")

        el = etree.Element('a')
        el.text = text
        el.set('href', ref)

        reference = create_or_none(ref)
        if reference is not None:
            links = self.find_matching_javadoc(reference)

            if len(links) == 0:
                logger.warning(f'No javadoc matching {ref} was found!')
                el.text = f'Invalid reference to {ref}'
            elif len(links) > 1:
                logger.warning(
                    f'Multiple javadoc matching {ref} found! Please be more specific, maybe add a pacakge? Found javadocs: {'; '.join(links)}')
                el.text = f'Invalid reference to {ref}'
            else:
                link, ref = next(iter(links.items()))
                el.set('href', link)
                return ref, el
        else:
            logger.debug(f"Invalid reference for {text} and {ref}")

        return None, el

    def find_matching_javadoc(self, reference) -> dict[str, Entity]:
        links = dict()
        for alias, site in self.sites.items():
            if reference.javadoc_alias is not None:
                if alias != reference.javadoc_alias: continue

            klasses = site.klasses_for_ref(reference)
            if klasses is None: continue
            links |= matches(klasses, reference)
        return links
