[![PyPI version](https://img.shields.io/pypi/v/markdown_javadoc_references?style=flat&link=!%5BPyPI%20-%20Version%5D(https%3A%2F%2Fimg.shields.io%2Fpypi%2Fv%2Fmarkdown_javadoc_references)
)](https://badge.fury.io/py/markdown_javadoc_references)
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

text = 'your markdown text with reference [String][java.lang.String]'
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
Referencing java methods, classes or fields is similar to how it is done in normal (markdown) javadoc comments,
with the slight change of double `[` and `]` in the second part of the reference.
For example
`[String#concat(String)][[String#concat(String)]]` will result in [String#concat(String)](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#concat(java.lang.String))

### Autolinks
Often times the text presented to the user can be easily derived from the used reference.
For this common case you can use the autolink syntax to avoid writing it twice.

`<String#concat(String)>` is the same as `[String#concat(String)][[String#concat(String)]]`

#### Formatting
By default, the text that is presented to the user is the reference with the packages stripped.

For example:
- `<java.lang.String>` -> `[String][[java.lang.String]])`
- `<java.lang.String#concat(java.lang.String)>` -> `[String#concat(String)][[java.lang.String#concat(java.lang.String)]]`
- `<java.lang.String#CASE_INSENSITIVE_ORDER` -> `[String#CASE_INSENSITIVE_ORDER][[java.lang.String#CASE_INSENSITIVE_ORDER]]`

To configure how the text is derived, you can provide a small python script via the config key `autolink-format`.
In this environment, you can use the `ref` variable to get the resolved [reference entity](src/markdown_javadoc_references/entities.py).
Now you can just use a `match` construct to define the specific formatting for each entity type.

The provided code then should just `return` the string presented to the user. 
The (class) names `Klass`, `Field` and `Method` are automatically imported for you. Please take a look at the [source code](src/markdown_javadoc_references/entities.py)
to learn more about the data and utility functions of each entity. You need some basic python programming skills to do this (or just ask ChatGPT).

> [!NOTE]
> The content of this config option will be copied in as the body of a python function.

Example (default formatter):
```python 
match ref:
    case Klass():
        return ref.name
    case Field():
        return f'{ref.klass.name}#{ref.name}'
    case Method():
        return f'{ref.klass.name}#{ref.name}({ref.parameter_names_joined()})'
```

Or in the `mkdocs.yml`:
```yaml
markdown_extensions:
  - markdown_javadoc_references:
      - urls:
          - 'https://docs.oracle.com/en/java/javase/24/docs/api/'
      - autolink-format: |
          match ref:
            case Klass():
              return ref.name
            case Field():
              return f'{ref.klass.name}#{ref.name}'
            case Method():
              return f'{ref.klass.name}#{ref.name}({ref.parameter_names_joined()})'
```

### Classes
To just reference a class you only need to provide its name:
`<String>`. If multiple classes with this name exists, just add a [package](#packages) or [url alias](#url-aliases).

### Methods
To reference methods you provide the classname and method name following its parameters separated by `#`:
`<String#conact(String)`.

Again, if multiple javadocs are matched just add a [url alias](#url-aliases) or [packages](#packages) to parameters
or the enclosing class.

### Packages
To clarify which class to use, you can add a package in front of it:
`<java.lang.String>`.

Furthermore, you can also a package to method parameters:
`<String#concact(java.lang.String)`

> [!WARNING]
> If multiple matches are found for a reference, the reference will be marked as "Invalid"!

### Fields
Like methods, fields can be referred to in a similar style `<String#CASE_INSENSITIVE_ORDER>` will link to [String#CASE_INSENSITIVE_ORDER](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/String.html#CASE_INSENSITIVE_ORDER)

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