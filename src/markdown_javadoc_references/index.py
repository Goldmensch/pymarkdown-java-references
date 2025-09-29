import json
import requests

# We have to cache them here, because mkdocs is loading markdown extensions multiple times
_index_cache = {}

def read_url(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

class Index:
    def __init__(self, urls):
        self.i_member = dict()
        self.i_pkg = dict()
        self.urls = tuple(urls)

        if self.urls in _index_cache:
            self.i_member, self.i_pkg = _index_cache[self.urls]
            return

        self.load_members()
        self.load_packages()

        _index_cache[self.urls] = (self.i_member, self.i_pkg)

    def load_members(self):
        for url in self.urls:
            text = read_url(url + '/member-search-index.js')
            json_text = text.removeprefix('memberSearchIndex = ').removesuffix(';updateSearchResults();').strip()
            data = json.loads(json_text)

            index = dict()
            for e in data:
                i = e['c']
                if i not in index:
                    index[i] = list()
                index[i].append(e)

            self.i_member[url] = index

    def load_packages(self):
        for url in self.urls:
            text = read_url(url + '/package-search-index.js')
            json_text = text.removeprefix('packageSearchIndex = ').removesuffix(';updateSearchResults();').strip()
            data = json.loads(json_text)

            index = dict()
            for e in data:
                index[e['l']] = e

            self.i_pkg[url] = index

    def module_name(self, url, pkg):
        e = self.i_pkg[url][pkg]
        if e['l'] == pkg and 'm' in e:
            return e['m']
        return None

    def url(self, pkg, klass, method):
        for e_url in self.i_member.items():
            classes = e_url[1].get(klass)
            if classes is None: continue
            for e in classes:
                if pkg is not None and (e['p'] != pkg): continue
                if method is not None and (e['l'] != method and not ('u' in e and e['u'] == method)): continue
                if e['c'] == klass:
                    return self.build_url(e_url[0], e, method is not None)
        return None

    def build_url(self, base, e, include_method):
        pkg: str = e['p']
        module = self.module_name(base, pkg)
        if module is not None: base = base + module + '/'
        base = base + pkg.replace('.', '/') + '/'
        base = base + e['c']

        base = base + '.html'

        if include_method:
            base = base + '#' + (e['u'] if 'u' in e else e['l'])

        return base