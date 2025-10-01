from functools import lru_cache

from .jdk8 import load as jdk8_load
from .jdk9 import load as jdk9_load
from .util import check_url


@lru_cache(maxsize=None)
def load(url):
    # /allclasses-noframe.html only exists pre java 9
    existing = check_url(f'{url}/allclasses-noframe.html')
    return jdk8_load(url) if existing else jdk9_load(url)
