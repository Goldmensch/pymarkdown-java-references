from .processor import JavaDocProcessor
from markdown.extensions import Extension


class JavaDocExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'urls': ['', 'A list of javadoc sites to search in.']
        }

        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(JavaDocProcessor(md, self.getConfig("urls")), 'javadoc_link_processor', 15)

def makeExtension(**kwargs):
    return JavaDocExtension(**kwargs)
