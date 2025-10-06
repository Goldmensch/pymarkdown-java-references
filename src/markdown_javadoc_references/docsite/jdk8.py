import urllib.parse

from bs4 import BeautifulSoup
from bs4.element import Tag

from .docsite import Docsite
from .util import read_url
from ..entities import *
from ..reference import Reference
from ..util import get_logger

logger = get_logger(__name__)

def load(url: str) -> Docsite:
    # info is intended
    logger.info(f'Loading java 8 docs.. may take a while: {url}')

    soup = BeautifulSoup(read_url(f'{url}/allclasses-noframe.html'), 'html.parser')

    klasses = dict()

    for anchor in soup.find('body').find('div').find('ul').select('a[href]'):
        klass = _load_class(url, anchor)

        # append subclasses as individual classes
        for name in klass.name.split('.'):
            klasses.setdefault(name, []).append(klass)

    return Jdk8(klasses)


# noinspection PyTypeChecker
def _load_class(url: str, c: Tag) -> Klass:
    logger.debug(f"Loading jdk8 class: {url}")
    name = c.get_text(strip=True)
    package = c.get('title').split()[-1]

    klass = Klass(None, package, name, None, None, f'{url}/{c.get('href')}')
    logger.debug(f'Loaded {package}.{name} from {klass.url}')

    return klass


def _load_members(url: str, klass: Klass):
    logger.debug(f"Loading members for: {klass}")

    text = read_url(url)
    klass.methods = list()
    klass.fields = list()

    soup = BeautifulSoup(text, "html.parser")
    anchors = {a.get("name") for a in soup.find_all("a", attrs={"name": True})}
    for a in anchors:
        parts = a.split('-')
        unquoted_url = urllib.parse.unquote(f'{url}#{a}')
        # first part is always name
        member_name = parts[0]

        # is field
        if len(parts) <= 1:
            klass.fields.append(Field(member_name, unquoted_url, klass))

        if member_name == klass.name: member_name = '<init>' # normalize constructor method names to <init>
        new_params = []

        # following parts are parameters
        for param in parts[1:]:

            # skip empty strings - they're not real parameters
            if len(param) == 0: continue

            # split at : - after it there are metadata like A for arrays
            name_split = param.split(':')
            new_name = name_split[0]

            # add [] for arrays
            if len(name_split) == 2:
                new_name = new_name + ('[]' * (name_split[1].count('A')))

            new_params.append(new_name.strip())


        klass.methods.append(Method(klass, member_name, new_params, unquoted_url))
    logger.debug(f"Found {len(klass.methods)} classes and {len(klass.fields)} fields for {klass.name} ({klass.url})")

class Jdk8(Docsite):
    def __init__(self, klasses):
        self.klasses = klasses

    # lazy load
    def klasses_for_ref(self, reference: Reference) -> list[Klass]:
        if reference.class_name not in self.klasses: return list()
        found = self.klasses[reference.class_name]

        found_names = list()
        for c in found:
            found_names.append(f" {c.name} -> {c.url}) ||")
        logger.debug(f"Found classes: {found_names} for reference {reference}")

        loaded = list()
        for klass in found:
            # none if unloaded
            if klass.methods is None:
                _load_members(klass.url, klass)
            loaded.append(klass)

        return loaded