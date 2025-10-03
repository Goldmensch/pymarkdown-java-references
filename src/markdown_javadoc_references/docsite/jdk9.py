import json
import logging
import urllib.parse

from .util import read_url
from ..entities import *

logger = logging.getLogger(__name__)


def load(url):
    logger.debug(f'Load java 9 doc: {url}')

    packages = load_packages(url)
    members = load_members(url)

    klasses =  load_classes(url, packages, members)
    return Jdk9(klasses)


def read_url_json(url, prefix):
    text = read_url(url)
    plain = text.removeprefix(prefix).removesuffix(';updateSearchResults();').strip()
    return json.loads(plain)


def find_module(name, pkgs):
    e = pkgs[name]
    if 'm' in e:
        return e['m']
    return None


def load_members(url):
    data = read_url_json(url + '/member-search-index.js', 'memberSearchIndex = ')

    index = dict()
    for e in data:
        if 'l' not in e or 'p' not in e: continue
        index.setdefault(f'{e['p']}.{e['c']}', list()).append(e)
    return index


def load_classes(url, pkgs, members):
    data = read_url_json(url + '/type-search-index.js', 'typeSearchIndex = ')
    klasses = dict()

    for e in data:
        # skip non member entries
        if 'l' not in e or 'p' not in e: continue
        name = e['l']
        package = e['p']
        module = find_module(package, pkgs)
        methods = list()
        fields = list()

        klass_url = build_klass_url(url, module, package, name)
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
                    methods.append(Method(klass, m_name, parameters, build_method_url(klass_url, m)))
                else: # is field
                    fields.append(Field(m_name, build_field_url(klass_url, m_name)))

        klasses.setdefault(name, list()).append(klass)

    return klasses


def build_klass_url(base, module, package, klass_name):
    # append module name if given
    if module is not None: base = f'{base}/{module}'
    # append package name
    base = f'{base}/{package.replace('.', '/')}'
    # append class name
    base = f'{base}/{klass_name}'

    # append .html
    return base + '.html'

def build_method_url(klass_url, m):
    return f'{klass_url}#{(m['u'] if 'u' in m else m['l'])}'

def build_field_url(klass_url, field_name):
    return f'{klass_url}#{field_name}'

def load_packages(url):
    data = read_url_json(url + '/package-search-index.js', 'packageSearchIndex = ')

    index = dict()
    for e in data:
        index[e['l']] = e
    return index

class Jdk9:
    def __init__(self, klasses):
        self.klasses = klasses

    def klasses_for_ref(self, reference):
        return self.klasses[reference.class_name] if reference.class_name in self.klasses else None