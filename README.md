# 🐍 Python Markdown Javadoc References
Have you ever been tired of copying entire Javadoc URLs into your Markdown just to link to the documentation for some Java classes?
That is where is extension comes in handy! 

This [python markdown extension](https://github.com/Python-Markdown/markdown) adds the ability to directly reference [Java](https://www.java.com/de/) classes, methods and fields in 
your markdown to link to their documentation. It supports both Javadoc prior to Java 9 and from Java 9 onwards.

## Installation
You can find the [extension on PyPi](https://pypi.org/project/markdown_javadoc_references/) under `markdown_javadoc_references`.

### With plain [python markdown](https://github.com/jackdewinter/pymarkdown)
To use this extension with the API of [python markdown](https://github.com/jackdewinter/pymarkdown), just add
`JavaDocRefExtension` to the list of your extensions and provide the URLs to use.

```python
import markdown
from markdown_javadoc_references import JavaDocRefExtension

urls = [
    'https://docs.oracle.com/en/java/javase/24/docs/api/',
    {
        'alias': 'jdk8',
        'url': 'https://docs.oracle.com/javase/8/docs/api/'
    }
]

text = 'your markdown text'
result = markdown.markdown(text, extensions=[JavaDocRefExtension(urls=urls)])
```


### With [MkDocs](https://www.mkdocs.org/)
To use this extension with [MkDocs](https://www.mkdocs.org/) just add it to your `mkdocs.yml`:

```yaml
markdown_extensions:
  - markdown_javadoc_references:
      - urls:
          - 'https://docs.oracle.com/en/java/javase/24/docs/api/'
          - alias: 'jdk8'
            url: 'https://docs.oracle.com/javase/8/docs/api/'
```

## Usage
Referencing java methods, classes or fields is similar to how it is done in normal javadoc comments, for example
`[String#concat(String)](String#concat(String))` will result in [String#concat(String)](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#concat(java.lang.String))

### Autolinks
Often times the text presented to the user is the same as the javadoc reference.
For this common case you can use the autolink syntax to avoid writing it twice.

`<String#concat(String)>` is the same as `[String#concat(String)](String#concat(String))`

### Packages
To clarify which class to use, you can add a package in front of it:
`<java.lang.String>`.

Furthermore, you can also a package to method parameters:
`<String#concact(java.lang.String)`

> [!WARNING]
> If multiple matches are found for a reference, the reference will be marked as "Invalid"!

### Fields
Like methods, fields can be referred to in a similar style with the small detail of double `#`: `<String##CASE_INSENSITIVE_ORDER>` will link to [String#CASE_INSENSITIVE_ORDER](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#CASE_INSENSITIVE_ORDER)

The double `#` is necessary to avoid conflicts with markdowns native headline linking.

### Constructors
To refer to constructors, just add `<init>` in the place where the method name would be:
`String#<init>(byte[],int,int)` will link to [String#<init>(byte[],int,int)](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#%3Cinit%3E(byte%5B%5D,int,int))

### URL aliases
Instead of stating the package explicitly, you can also add a URL alias to your reference.
For that to work, you have to state the alias for your javadoc site in your [configuration. (take a look at installation)](#installation)

Assuming you have a javadoc site configured with the alias "jdk8":
```yaml
markdown_extensions:
  - markdown_javadoc_references:
      - urls:
        - 'https://docs.oracle.com/en/java/javase/24/docs/api/'
        - alias: 'jdk8'
          url: 'https://docs.oracle.com/javase/8/docs/api/'
```

you can now use this alias to force the extension to only search under the site `https://docs.oracle.com/javase/8/docs/api/`
for the referred to javadoc: `<jdk8 -> String#<init>(byte[],int,int)>` 

Additionally, if you don't have an alias configured explicitly, you can still use the whole URL:
`<https://docs.oracle.com/en/java/javase/24/docs/api/ -> String#<init>(byte[],int,int)>`

> [!IMPORTANT]
> The URL has to be still mentioned in the configuration!