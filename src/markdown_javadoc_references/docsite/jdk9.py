import json
import urllib.parse

from .docsite import Docsite
from .util import read_url
from ..entities import Klass, Method, Field
from ..reference import Reference
from ..util import get_logger

logger = get_logger(__name__)

def load(url: str) -> Docsite:
    logger.debug(f'Loading java 9 doc: {url}')

    packages = _load_packages(url)
    members = _load_members(url)

    klasses =  _load_classes(url, packages, members)
    return Jdk9(klasses)


def _read_url_json(url: str, prefix: str) -> list[dict[str, str]]:
    text = read_url(url)
    plain = text.removeprefix(prefix).removesuffix(';updateSearchResults();').strip()
    return json.loads(plain)


def _find_module(name: str, pkgs: dict[str, dict[str, str]]) -> str | None:
    e = pkgs[name]
    if 'm' in e:
        return e['m']
    return None


def _load_members(url: str) -> dict[str, list[dict[str, str]]]:
    logger.debug(f"Load members for {url}")

    data = _read_url_json(url + '/member-search-index.js', 'memberSearchIndex = ')

    index = dict()
    for e in data:
        if 'l' not in e or 'p' not in e:
            continue
        index.setdefault(f'{e["p"]}.{e["c"]}', list()).append(e)
    return index


def _load_classes(url: str, pkgs: dict[str, dict[str, str]], members: dict[str, list[dict[str, str]]]) -> dict[str, list[Klass]]:
    logger.debug(f"Load classes for {url}")

    data = _read_url_json(url + '/type-search-index.js', 'typeSearchIndex = ')
    klasses = dict()

    for e in data:
        # skip non member entries
        if 'l' not in e or 'p' not in e:
            continue
        name = e['l']
        package = e['p']
        module = _find_module(package, pkgs)
        methods = list()
        fields = list()

        klass_url = _build_klass_url(url, module, package, name)
        klass = Klass(module, package, name, methods, fields, klass_url)

        i = f'{package}.{name}'

        # check if class has members
        if i in members:

            # get through all members of class
            for m in members[i]:
                # u in only included if reference types are parameters. No parameters + only primitives -> l
                index = 'u' if 'u' in m else 'l'
                m_name = urllib.parse.unquote(m[index].split('(', 1)[0])  ## get name -> split at ( and get first half
                parameters = list()

                raw = m[index]
                if '(' in raw:  # just exclude fields for now
                    u_split = raw.split('(', 1)[1].removesuffix(')')
                    if len(u_split) != 0:
                        for p in u_split.split(','):
                            parameters.append(p.strip())
                    methods.append(Method(klass, m_name, parameters, _build_method_url(klass_url, m)))
                else: # is field
                    fields.append(Field(m_name, _build_field_url(klass_url, m_name), klass))

        # append subclasses as individual classes
        for s_name in name.split('.'):
            klasses.setdefault(s_name, list()).append(klass)

    return klasses


def _build_klass_url(base: str, module: str | None, package: str, klass_name: str) -> str:
    # append module name if given
    if module is not None:
        base = f'{base}/{module}'
    # append package name
    base = f"{base}/{package.replace('.', '/')}"
    # append class name
    base = f'{base}/{klass_name}'

    # append .html
    return base + '.html'

def _build_method_url(klass_url: str, m: dict[str, str]) -> str:
    return f"{klass_url}#{(m['u'] if 'u' in m else m['l'])}"

def _build_field_url(klass_url: str, field_name: str) -> str:
    return f'{klass_url}#{field_name}'

def _load_packages(url: str) -> dict[str, dict[str, str]]:
    logger.debug(f"Load packages for {url}")

    data = _read_url_json(url + '/package-search-index.js', 'packageSearchIndex = ')

    index = dict()
    for e in data:
        index[e['l']] = e
    return index

class Jdk9(Docsite):
    def __init__(self, klasses: dict[str, list[Klass]]):
        self.klasses = klasses

    def klasses_for_ref(self, reference: Reference) -> list[Klass]:
        return self.klasses[reference.class_name] if reference.class_name in self.klasses else list()