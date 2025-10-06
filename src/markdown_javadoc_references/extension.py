from markdown.core import Markdown
from markdown.extensions import Extension

from .processor.javadoc import JavaDocProcessor
from .processor.autolink import AutoLinkJavaDocProcessor
from .resolver import Resolver
from .util import get_logger

logger = get_logger(__name__)

class JavaDocRefExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'urls': [[], 'A list of javadoc sites to search in.'],
            'autolink-format': ['', 'A python expression to produce the text of autolinks presented to the user.']
        }

        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown):
        logger.debug("extendMarkdown called.. (JavaDocRefExtension)")

        resolver = Resolver(self.getConfig("urls"))

        logger.debug("Registering extension processors..")
        md.inlinePatterns.register(AutoLinkJavaDocProcessor(md, resolver, self.getConfig("autolink-format")), 'javadoc_reference_autolink_processor', 140)
        md.inlinePatterns.register(JavaDocProcessor(md, resolver), 'javadoc_reference_processor', 140)
