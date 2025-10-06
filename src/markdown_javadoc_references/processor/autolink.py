import re

from ..reference import raw_pattern as ref_pattern
from markdown.inlinepatterns import InlineProcessor

from ..entities import Klass, Field, Method
from ..util import get_logger

logger = get_logger(__name__)

def default_formatter(ref):
    match ref:
        case Klass():
            return ref.name
        case Field():
            return f'{ref.klass.name}#{ref.name}'
        case Method():
            return f'{ref.klass.name}#{ref.name}({ref.parameter_names_joined()})'
        case _:
            raise ValueError("Should not occur")

def compile_formatter(code: str):
    namespace = {
        "Klass": Klass,
        "Method": Method,
        "Field": Field
    }

    indented = '\n'.join("  " + line for line in code.splitlines())

    wrapper = f"def autolink_format(ref): \n{indented}\n"

    exec(wrapper, namespace)
    return namespace["autolink_format"]

auto_link_pattern = rf'<(?!init>)({ref_pattern[:-1]})>'

class AutoLinkJavaDocProcessor(InlineProcessor):
    def __init__(self, md, resolver, autolink_format: str):
        super().__init__(auto_link_pattern, md)
        self.resolver = resolver
        self.formatter = compile_formatter(autolink_format) if autolink_format != '' else None

    def handleMatch(self, m, data):
        logger.debug(f"Handle auto link match: {m.group(0)}")

        ref, el = self.resolver.resolve(m.group('whole_ref'), m.group(1))
        if ref is not None:
            try:
                formatted = self.formatter(ref) if self.formatter is not None else default_formatter(ref)
            except Exception as e:
                logger.error(f"Error while evaluating autolink ({el.get('href')}): {e}")
                formatted = el.get('href')

            el.text = formatted

        return el, m.start(0), m.end(0)
