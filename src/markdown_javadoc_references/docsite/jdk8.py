import logging
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

from .util import read_url
from ..entities import *

logger = logging.getLogger(__name__)


def load(url):
    # info is intended
    logger.info(f'Loading java 8 docs.. may take a while: {url}')

    soup = BeautifulSoup(read_url(f'{url}/allclasses-noframe.html'), 'html.parser')

    klasses = dict()

    for anchor in soup.find('body').find('div').find('ul').select('a[href]'):
        klass = load_class(url, anchor)
        klasses.setdefault(klass.name, []).append(klass)

    return Jdk8(klasses)


def load_class(url, c):
    name = c.get_text(strip=True)
    package = c.get('title').split()[-1]

    klass = Klass(None, package, name, None, f'{url}/{c.get('href')}')
    logger.info(f'Loading {package}.{name} from {klass.url}')

    return klass


def load_members(url, methods, klass):
    text = read_url(url)

    soup = BeautifulSoup(text, "html.parser")
    anchors = {a.get("name") for a in soup.find_all("a", attrs={"name": True})}
    for a in anchors:
        parts = a.split('-')
        if len(parts) <= 1: continue

        # first part is always name
        method = parts[0]
        if method == klass.name: method = '<init>' # normalise constructor method names to <init>
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

        unquoted_url = urllib.parse.unquote(f'{url}#{a}')
        methods.append(Method(klass, method, new_params, unquoted_url))

class Jdk8:
    def __init__(self, klasses):
        self.klasses = klasses

    # lazy load
    def klasses_for_ref(self, reference):
        found = self.klasses[reference.class_name]

        loaded = list()
        for klass in found:
            if klass.methods is None:
                methods = list()
                load_members(klass.url, methods, klass)
                klass.methods = methods
            loaded.append(klass)

        return loaded