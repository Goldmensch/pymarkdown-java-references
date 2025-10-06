import re


class Klass:
    """
    Represents a resolved reference class.

    Attributes
    ----------
    module : str
        The module name or None if not existing
    package : str
        The package name
    name : str
        The class name
    methods : list[Method]
        The methods of this class
    fields : list[Field]
        The fields/enum constants of this class
    url : str
        The url pointing to the javadoc site of this class
    """

    def __init__(self, module, package, name, methods, fields, url):
        self.module = module
        self.package = package
        self.name = name
        self.methods = methods
        self.url = url
        self.fields = fields

class Field:
    """
    Represents a resolved reference to a field.

    Attributes
    ----------
    name : str
        The name of this field.
    url : str
        The url pointing to the javadoc site of this field
    klass : Klass
        The enclosing class of this field.
    """


    def __init__(self, name, url, klass):
        self.klass = klass
        self.name = name
        self.url = url

class Method:
    """
    Represents a resolved reference to a method.

    Attributes
    ----------
    name : str
        The name of this method
    parameters : list[String]
        The parameters of this method, consisting of full qualified names including the package.
    klass : Klass
        The enclosing class of this method
    url : str
        The url pointing to the javadoc site of this method.

    Methods
    -------
    parameter_names()
        Returns a list of parameters, with their package stripped by convention.

        According to the java conventions, packages are lower case and class names start with an upper case character.
        That means, that the parameter `java.lang.String` will be stripped to `String`.
        The parameter `my.package.MyClass.SubClass` for example, will be stripped to `MyClass.SubClass`

    parameter_names_joined()
        Returns a string consisting of the parameter names from `parameter_names()` joined together by `, `
    """

    def __init__(self, klass, name, parameters, url):
        self.klass = klass
        self.name = name
        self.parameters = parameters
        self.url = url

    def parameter_names(self):
        params = list()
        for p in self.parameters:
            matched = re.search(r"[A-Z]", p)
            if matched:
                i = matched.start()
                params.append(p[i:])
            else:
                params.append(p)
        return params

    def parameter_names_joined(self):
        return ", ".join(self.parameter_names())
