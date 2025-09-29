## review note: just let this file here for future testing
import markdown
from markdown_javadoc_references import JavaDocRefExtension

def compare(expected, input):
    urls = [
        'https://docs.oracle.com/en/java/javase/24/docs/api/'
    ]

    result = markdown.markdown(input, extensions=[JavaDocRefExtension(urls=urls)])


    assert "<a " in result, f"No link parsed from: {input!r}"

    assert expected == result

def test_only_class():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html">String</a></p>'
    compare(expected, "[String](String)")

def test_class_with_package():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html">String</a></p>'
    compare(expected, "[String](java.lang.String)")

def test_class_with_function_without_parameter():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#trim()">String</a></p>'
    compare(expected, "[String](String#trim())")

def test_class_with_function_with_parameter_primitive():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#substring(int)">String</a></p>'
    compare(expected, "[String](String#substring(int))")

def test_class_with_function_with_parameter_object():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#lastIndexOf(java.lang.String)">String</a></p>'
    compare(expected, "[String](String#lastIndexOf(String))")

def test_class_with_function_with_parameter_object_and_primitive():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#lastIndexOf(java.lang.String,int)">String</a></p>'
    compare(expected, "[String](String#lastIndexOf(String, int))")
