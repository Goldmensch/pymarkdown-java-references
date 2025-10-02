import re

raw_pattern = r'([\w.]*\.)?(\w+)(?:#(<?\w+>?)\((.*)\))?$'
pattern = re.compile(raw_pattern)

def create_or_none(raw):
    match = pattern.match(raw)
    return Reference(match) if match else None


class Reference:
    def __init__(self, match: re.Match):
        """
        regex will match: java.util.com.MyClass#foo(String,int,boolean) -->
        group 1: package (optional)
        group 2: class name
        group 3: method name (optional, together with parameters)
        group 4: parameters (optional, together with method name)
        """
        self.package = match.group(1)
        if self.package is not None: self.package = self.package.removesuffix('.')

        self.class_name = match.group(2)
        self.method_name = match.group(3)

        self.parameters = list()

        parameter = match.group(4)
        if parameter is not None and parameter != '':
            for par in parameter.split(','):
                self.parameters.append(par.strip())
