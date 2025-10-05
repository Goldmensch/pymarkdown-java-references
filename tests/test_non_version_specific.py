import markdown
from markdown_javadoc_references import JavaDocRefExtension

default_urls = [
    'https://docs.oracle.com/en/java/javase/24/docs/api/',
]

def compare(expected, text, urls=default_urls):
    result = markdown.markdown(text, extensions=[JavaDocRefExtension(urls=urls)])

    assert result == expected

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

def test_autolink_in_codeblock():
    expected = '<p><code>&lt;String#join(CharSequence, CharSequence...)&gt;</code></p>'
    compare(expected, "`<String#join(CharSequence, CharSequence...)>`")

def test_javadoc_alias_whole_url():
    urls = [
        'https://docs.oracle.com/en/java/javase/24/docs/api/',
        'https://docs.oracle.com/javase/8/docs/api/'
    ]

    expected = '<p><a href="https://docs.oracle.com/javase/8/docs/api/java/lang/String.html">String</a></p>'
    compare(expected, "<https://docs.oracle.com/javase/8/docs/api/ -> String>", urls)

def test_javadoc_alias_custom_alias():
    urls = [
        'https://docs.oracle.com/en/java/javase/24/docs/api/',
        {
            'alias': 'jdk8',
            'url': 'https://docs.oracle.com/javase/8/docs/api/'
        }
    ]

    expected = '<p><a href="https://docs.oracle.com/javase/8/docs/api/java/lang/String.html">String</a></p>'
    compare(expected, "<jdk8 -> String>", urls)


def test_site_not_found():
    urls = [
        'https://notworkingdocs.com',
    ]

    expected = '<p><a href="jdk8 -&gt; String">Invalid reference to jdk8 -&gt; String</a></p>'
    compare(expected, "<jdk8 -> String>", urls)