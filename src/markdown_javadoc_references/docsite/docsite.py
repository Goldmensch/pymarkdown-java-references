
from functools import lru_cache

import requests.exceptions

from .util import check_url
from ..entities import Klass
from ..util import get_logger

logger = get_logger(__name__)

class Docsite:
    def klasses_for_ref(self, reference) -> list[Klass]:
        pass

@lru_cache(maxsize=None)
def load(url: str) -> Docsite | None:
    from .jdk8 import load as jdk8_load
    from .jdk9 import load as jdk9_load

    # check if url is reachable
    try:
        resp = check_url(url)
        if not resp.ok:
            logger.error(f"Couldn't open site {url}, got {resp.status_code} - skipping it... Perhaps misspelled?")
            return None
    except requests.exceptions.RequestException:
        logger.error(f"Couldn't open site {url} - skipping it... Perhaps misspelled?")
        return None

    # /allclasses-noframe.html only exists pre java 9
    existing = check_url(f'{url}/allclasses-noframe.html')
    return jdk8_load(url) if existing.ok else jdk9_load(url)
