import re

from markdown.treeprocessors import Treeprocessor

from .index import Index

def if_given(value, func):
    if value is not None:
        return func(value)
    else:
        return None

class JavaDocProcessor(Treeprocessor):
    def __init__(self, md, urls):
        super().__init__(md)

        self.index = Index(urls)


    def run(self, root):
        """
        regex will match: java.util.com.MyClass#foo(String,int,boolean) -->
        group 1: package (optional)
        group 2: class name
        group 3: method name + parameters (optional)
        """

        pattern = re.compile(r'([\w.]*\.)?(\w+)(?:#(\w+\(.*\)))?$')
        for el in root.iter('a'):
            href = el.get('href', '')
            m = pattern.match(href)
            if m:
                pkg = if_given(m.group(1), lambda x: x.removesuffix('.'))
                url = self.index.url(pkg, m.group(2), m.group(3))

                final_text = 'Invalid' if url is None else url
                el.set('href', final_text)