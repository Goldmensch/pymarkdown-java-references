import markdown
from markdown_javadoc_references import JavaDocRefExtension

default_urls = [
    'https://docs.oracle.com/en/java/javase/24/docs/api/',
]

def compare(expected, text, urls=default_urls):
    result = markdown.markdown(text, extensions=[JavaDocRefExtension(urls=urls)])

    assert expected == result

### non version specific tests
def test_normal_autolink_still_work():
    expected = '<p><a href="https://www.google.com">https://www.google.com</a></p>'
    compare(expected, "<https://www.google.com>")

def test_autolink_only_class():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html">String</a></p>'
    compare(expected, "<String>")

def test_autolink_with_parameters():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#join(java.lang.CharSequence,java.lang.CharSequence...)">String#join(CharSequence, CharSequence...)</a></p>'
    compare(expected, "<String#join(CharSequence, CharSequence...)>")