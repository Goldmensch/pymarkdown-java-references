from markdown.extensions import Extension

from .processor import JavaDocProcessor, AutoLinkJavaDocProcessor


class JavaDocRefExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'urls': [[], 'A list of javadoc sites to search in.']
        }

        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(JavaDocProcessor(md, self.getConfig("urls")), 'javadoc_reference_processor', 15)

        md.inlinePatterns.register(AutoLinkJavaDocProcessor(md), 'javadoc_reference_autolink_processor', 140)
