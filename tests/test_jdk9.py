## review note: just let this file here for future testing
import markdown
from markdown_javadoc_references import JavaDocRefExtension

default_urls = [
    'https://docs.oracle.com/en/java/javase/24/docs/api/',
]

def compare(expected, text, urls=default_urls):
    result = markdown.markdown(text, extensions=[JavaDocRefExtension(urls=urls)])

    assert expected == result

def test_without_module():
    urls = [
        'https://docs.jda.wiki/'
    ]

    expected = '<p><a href="https://docs.jda.wiki/net/dv8tion/jda/api/JDA.html">JDA</a></p>'
    compare(expected, '[JDA](JDA)', urls)


def test_field_reference():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#CASE_INSENSITIVE_ORDER">String#CASE_INSENSITIVE_ORDER</a></p>'
    compare(expected, "<String#CASE_INSENSITIVE_ORDER>")

def test_constructor_with_parameters():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#%3Cinit%3E(byte[],int,int,java.nio.charset.Charset)">String</a></p>'
    compare(expected, "[String](String#<init>(byte[],int,int,java.nio.charset.Charset))")

def test_constructor_without_parameters():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#%3Cinit%3E()">String</a></p>'
    compare(expected, "[String](String#<init>())")

def test_only_class():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html">String</a></p>'
    compare(expected, "[String](String)")

def test_class_with_package():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html">String</a></p>'
    compare(expected, "[String](java.lang.String)")

def test_class_with_function_without_parameter():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#trim()">String</a></p>'
    compare(expected, "[String](String#trim())")

def test_class_with_function_without_parameter_not_existing():
    expected = '<p><a href="String#notexisting()">Invalid reference to String#notexisting()</a></p>'
    compare(expected, "[String](String#notexisting())")

def test_class_with_function_with_parameter_primitive():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#substring(int)">String</a></p>'
    compare(expected, "[String](String#substring(int))")

def test_class_with_function_with_parameter_object():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#lastIndexOf(java.lang.String)">String</a></p>'
    compare(expected, "[String](String#lastIndexOf(String))")

def test_class_with_function_with_parameter_object_and_primitive():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#lastIndexOf(java.lang.String,int)">String</a></p>'
    compare(expected, "[String](String#lastIndexOf(String, int))")

def test_class_with_vararg_parameter():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#join(java.lang.CharSequence,java.lang.CharSequence...)">String</a></p>'
    compare(expected, "[String](String#join(CharSequence, CharSequence...))")

def test_class_with_array():
    expected = '<p><a href="https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#copyValueOf(char[],int,int)">String</a></p>'
    compare(expected, "[String](String#copyValueOf(char[], int, int))")


