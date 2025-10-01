import logging
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

from .util import read_url
from ..entities import *

logger = logging.getLogger(__name__)


def load(url):
    # info is intended
    logger.info(f'Loading java 8 docs.. may take a while: {url}')

    soup = BeautifulSoup(read_url(f'{url}/allclasses-noframe.html'), 'html.parser')

    class_list = soup.find('body').find('div').find('ul').select('a[href]')

    with ThreadPoolExecutor() as pool:
        results = list(pool.map(lambda c: load_class(url, c), class_list))

    klasses = dict()
    for klass in results:
        klasses.setdefault(klass.name, []).append(klass)

    return klasses


def load_class(url, c):
    name = c.get_text(strip=True)
    package = c.get('title').split()[-1]
    methods = list()

    klass = Klass(None, package, name, methods, f'{url}/{c.get('href')}')
    logger.info(f'Loading {package}.{name} from {klass.url}')

    load_members(klass.url, methods, klass)

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

        methods.append(Method(klass, method, new_params, f'{url}#{a}'))
