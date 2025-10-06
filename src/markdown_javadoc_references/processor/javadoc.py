from markdown.inlinepatterns import InlineProcessor

from ..reference import raw_pattern as ref_pattern
from ..util import get_logger

logger = get_logger(__name__)

java_doc_pattern = rf'\[(.*)\]\[\[({ref_pattern[:-1]})\]\]'
class JavaDocProcessor(InlineProcessor):
    def __init__(self, md, resolver):
        super().__init__(java_doc_pattern, md)
        self.resolver = resolver

    def handleMatch(self, m, data):
        logger.debug(f"Handle explict link match: {m.group(0)}")
        _, el = self.resolver.resolve(m.group(1), m.group(2))
        return el, m.start(0), m.end(0)
