import logging

from markdown.inlinepatterns import InlineProcessor

from .reference import raw_pattern as ref_pattern

logger = logging.getLogger(__name__)

java_doc_pattern = rf'\[(.*)\]\[\[({ref_pattern[:-1]})\]\]'
class JavaDocProcessor(InlineProcessor):
    def __init__(self, md, resolver):
        super().__init__(java_doc_pattern, md)
        self.resolver = resolver

    def handleMatch(self, m, data):
        return self.resolver.resolve(m.group(1), m.group(2)), m.start(0), m.end(0)


auto_link_pattern = rf'<({ref_pattern[:-1]})>$'
class AutoLinkJavaDocProcessor(InlineProcessor):
    def __init__(self, md, resolver):
        super().__init__(auto_link_pattern, md)
        self.resolver = resolver

    def handleMatch(self, m, data):
        return self.resolver.resolve(m.group('whole_ref'), m.group(1)), m.start(0), m.end(0)
