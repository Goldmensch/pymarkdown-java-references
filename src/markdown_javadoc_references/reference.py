from enum import Enum

import re

raw_pattern = r'(?:(?P<doc>.+) *-> *)?(?P<whole_ref>(?P<pkg>[\w.]*\.)?(?P<klass>\w+)(?:#(?:(?P<method><?\w+>?)\((?P<params>.*)\))|(?:##(?P<field>\w+)))?)$'
pattern = re.compile(raw_pattern)

def create_or_none(raw):
    match = pattern.match(raw)
    return Reference(match) if match else None


class Reference:
    def __init__(self, match: re.Match):
        """
        regex will match: alias -> java.util.com.MyClass#foo(String,int,boolean) -->

        group doc: javadoc alias name
        group pkg: package (optional)
        group klass: class name
        group method: method name (optional, together with parameters)
        group params: parameters (optional, together with method name)

        if field reference: java.util.com.MyClass#MY_FIELD
        group field: field name
        """

        self.javadoc_alias = match.group('doc')
        if self.javadoc_alias is not None:
            self.javadoc_alias = self.javadoc_alias.strip()

        self.package = match.group('pkg')
        if self.package is not None: self.package = self.package.removesuffix('.')

        self.class_name = match.group('klass')

        if match.group('field') is None:
            self.member_name = match.group('method')

            self.parameters = list()

            parameter = match.group('params')
            if parameter is not None and parameter != '':
                for par in parameter.split(','):
                    self.parameters.append(par.strip())
            self.type = Type.METHOD
        else:
            self.type = Type.FIELD
            self.member_name = match.group('field')

class Type(Enum):
    METHOD = 1
    FIELD = 2