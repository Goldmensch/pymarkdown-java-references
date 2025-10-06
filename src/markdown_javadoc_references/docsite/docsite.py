from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import Callable

import requests.exceptions

from .util import check_url
from ..entities import Klass
from ..util import get_logger

logger = get_logger(__name__)

executor = ThreadPoolExecutor(max_workers=32)

class Docsite:
    def __init__(self, klasses: dict[str, list[Klass]], lazy_load: Callable[[Klass], None]):
        self.klasses = klasses
        self._klasses_for_ref_cached = lru_cache(maxsize=None)(self._klasses_for_ref_uncached)
        self._lazy_load = lazy_load

    def klasses_for_ref(self, class_name: str) -> list[Klass]:
        return self._klasses_for_ref_cached(class_name)

    # lazy load done here
    def _klasses_for_ref_uncached(self, class_name: str) -> list[Klass]:
        if class_name not in self.klasses:
            return list()
        found = self.klasses[class_name]

        found_names = list()
        for c in found:
            found_names.append(f" {c.name} -> {c.url}) ||")
        logger.debug(f"Found classes: {found_names} for reference {class_name}")

        found = self.klasses[class_name]

        def ensure_members(klass: Klass):
            if klass.type is None:
                self._lazy_load(klass)
            return klass

        found = list(executor.map(ensure_members, found))

        return found

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
