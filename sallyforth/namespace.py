from util import get_attribute
from wrappers import value_f
from module_loader import load_module

class Var:
    """
    A Var is a named container for a value.
    Vars contain the name, the value and a dynamic flag,
    which indicates if the value is static or should be looked
    up anew for each use.

    Since the major use for Vars is to store the functions
    associated with Forth words, Vars can also proxy many
    of the methods of a Forth word.
    """

    def __init__(self, name, value, dynamic=True):
        self.name = name
        self.value = value
        self.dynamic = dynamic

    def __call__(self, forth):
        return self.value(forth)

    @property
    def immediate(self):
        return self.value.immediate

    @property
    def contents(self):
        return self.value.contents

    @property
    def operation_type(self):
        return self.value.operation_type

    def __str__(self):
        return f' Var({self.name}/{self.dynamic}::{self.value}) '

    def __repr__(self):
        return str(self)

class Namespace:
    """
    A Namespace is basically a string name -> function dictionary.
    Namespaces also know about includes which are a list of other
    namespaces.

    When you look up a name in a namespace it first looks in its
    own dictionary (contents) and then searchs its includes, in
    the order in which they were included.
    """

    def __init__(self, name, includes=[]):
        self.includes = includes.copy()
        self.contents = {}
        self.name = name

    def include_ns(self, other):
        self.includes.append(other)

    def alias(self, new_name, existing_name):
        self.contents[new_name] = self.contents[existing_name]

    def import_from_module(self, module_name):
        """
        Import all of the word defining functions in module m.
        """
        m = load_module(module_name)
        names = dir(m)
        for name in names:
            value = getattr(m, name)
            if get_attribute(value, 'forth_word'):
                forth_name = value.forth_name or name
                if forth_name in self:
                    print("Warning: redefining", forth_name)
                var = self.set(forth_name, value, False)

    def import_native_module(self, m, alias=None):
        if not alias:
            alias = m.__name__
            alias = alias.replace(".", "/")
    
        names = dir(m)
        for name in names:
            localname = f'{alias}/{name}'
            val = getattr(m, name)
            var = self.set(localname, value_f(val), False)

    def set(self, key, value, dynamic=True):
        if key not in self.contents:
            var = Var(key, value, dynamic)
            self.contents[key] = var
        else:
            var = self.contents[key]
            var.value = value
            var.dynamic = dynamic
        return var

    def set_constant(self, key, value):
        return self.set(key, value_f(value))

    def keys(self):
        return self.contents.keys()

    def all_keys(self):
        result = set(self.contents.keys())
        for h in self.includes:
            result = result.union(set(h.keys()))
        return result

    def private_contains(self, key):
        return self.contents.__contains__(key)

    def __contains__(self, key):
        if key in self.contents:
            return True
        for h in self.includes:
            if key in h:
                return True
        return False

    def __delitem__(self, key):
        return self.contents.__delitem__(key)

    def __setitem__(self, key, x):
        return self.set(key, x)

    def __iter__(self):
        return self.contents.__iter__()

    def private_lookup(self, key):
        return self.contents[key]

    def __getitem__(self, key):
        if key in self.contents:
            return self.contents[key]
        for h in self.includes:
            if key in h:
                return h[key]
        raise KeyError(key)

    def __str__(self):
        return f'Namespace({self.name})'
