import markdown

from markdown_javadoc_references import JavaDocRefExtension

def compare(expected, text, urls, autolink_format=''):
    result = markdown.markdown(text, extensions=[JavaDocRefExtension(urls=urls, **{'autolink-format': autolink_format})])

    assert result == expected

def test_specific_version():
    urls = [
        'https://javadoc.io/doc/com.zaxxer/HikariCP/7.0.1/'
    ]

    expected = '<p><a href="https://javadoc.io/static/com.zaxxer/HikariCP/7.0.1/com/zaxxer/hikari/HikariDataSource.html">HikariDataSource</a></p>'
    compare(expected, "<HikariDataSource>", urls=urls)

def test_latest():
    urls = [
        'https://javadoc.io/doc/com.zaxxer/HikariCP/latest/index.html'
    ]

    expected = '<p><a href="https://javadoc.io/static/com.zaxxer/HikariCP/7.0.2/com/zaxxer/hikari/HikariDataSource.html">HikariDataSource</a></p>'
    compare(expected, "<HikariDataSource>", urls=urls)