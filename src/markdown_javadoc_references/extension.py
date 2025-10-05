from markdown.extensions import Extension

from .processor import JavaDocProcessor, AutoLinkJavaDocProcessor
from .resolver import Resolver


class JavaDocRefExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'urls': [[], 'A list of javadoc sites to search in.']
        }

        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        resolver = Resolver(self.getConfig("urls"))

        md.inlinePatterns.register(AutoLinkJavaDocProcessor(md, resolver), 'javadoc_reference_autolink_processor', 140)
        md.inlinePatterns.register(JavaDocProcessor(md, resolver), 'javadoc_reference_processor', 140)
