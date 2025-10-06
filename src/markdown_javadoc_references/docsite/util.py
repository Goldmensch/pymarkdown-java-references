import requests

from markdown_javadoc_references.entities import Klass, Type
from markdown_javadoc_references.util import get_logger

logger = get_logger(__name__)

def read_url(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def check_url(url: str) -> requests.Response:
    resp = requests.head(url)
    return resp

def find_class_type(text: str, klass: Klass) -> Type | None:
    match text:
        case s if "Enum" in s:
            return Type.ENUM
        case s if "Annotation" in s:
            return Type.ANN_INTERFACE
        case s if "Interface" in s:
            return Type.INTERFACE
        case s if "Record" in s:
            return Type.RECORD
        case s if "Class" in s:
            return Type.CLASS
        case _:
            logger.error(f"Unknown class type in title {text} of {klass.url}")
            return None