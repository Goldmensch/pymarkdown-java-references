import re
from collections.abc import Callable
from typing import cast

from ..reference import raw_pattern as ref_pattern
from markdown.inlinepatterns import InlineProcessor

from ..entities import Klass, Field, Method, Entity
from ..resolver import Resolver
from ..util import get_logger

logger = get_logger(__name__)

def _default_formatter(ref: Entity) -> str:
    match ref:
        case Klass():
            return ref.name
        case Field():
            return f'{ref.klass.name}#{ref.name}'
        case Method():
            return f'{ref.klass.name}#{ref.name}({ref.parameter_names_joined()})'
        case _:
            raise ValueError("Should not occur")

def _compile_formatter(code: str) -> Callable[[Entity], str]:
    namespace = {
        "Klass": Klass,
        "Method": Method,
        "Field": Field,
        "Entity": Entity
    }

    indented = '\n'.join("  " + line for line in code.splitlines())

    wrapper = f"def autolink_format(ref: Entity) -> str:  \n{indented}\n"

    exec(wrapper, namespace)
    return cast(Callable[[Entity], str], namespace["autolink_format"])

auto_link_pattern: str = rf'<(?!init>)({ref_pattern[:-1]})>'

class AutoLinkJavaDocProcessor(InlineProcessor):
    def __init__(self, md, resolver: Resolver, autolink_format: str):
        super().__init__(auto_link_pattern, md)
        self.resolver = resolver
        self.formatter = _compile_formatter(autolink_format) if autolink_format != '' else _default_formatter

    def handleMatch(self, m: re.Match, data: str):
        logger.debug(f"Handle auto link match: {m.group(0)}")

        ref, el = self.resolver.resolve(m.group('whole_ref'), m.group(1))
        if ref is not None:
            try:
                formatted = self.formatter(ref)
            except Exception as e:
                logger.error(f"Error while evaluating autolink ({el.get('href')}): {e}")
                formatted = el.get('href')

            el.text = formatted

        return el, m.start(0), m.end(0)
