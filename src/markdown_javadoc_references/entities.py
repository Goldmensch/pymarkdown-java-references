class Klass:
    def __init__(self, module, package, name, methods, url):
        self.module = module
        self.package = package
        self.name = name
        self.methods = methods
        self.url = url


class Method:
    def __init__(self, klass, name, parameters, url):
        self.klass = klass
        self.name = name
        self.parameters = parameters
        self.url = url
