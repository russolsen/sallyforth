from util import get_attribute
from wrappers import value_f
from recoder import load_module

class Var:
    def __init__(self, name, value, dynamic=True):
        self.name = name
        self.value = value
        self.dynamic = dynamic

    def __str__(self):
        return f'[[[[Var({self.name}/{self.dynamic}::{self.value})]]]'

    def __repr__(self):
        return str(self)

class Namespace:
    def __init__(self, name):
        self.contents = {}
        self.name = name

    def alias(self, new_name, existing_name):
        self.contents[new_name] = self.contents[existing_name]

    def import_from_module(self, module_name):
        """
        Import all of the word defining functions in
        module m whose function names start with prefix
        into this namespace. Removes the prefix.
        """
        m = load_module(module_name)
        print(m)
        names = dir(m)
        for name in names:
            value = getattr(m, name)
            print("IMP", name, value, '=>', getattr(value, 'ast', None))
            if get_attribute(value, 'forth_word'):
                forth_name = value.forth_name or name
                var = self.set(forth_name, value, False)
                #var.immediate = value.forth_immediate
                #print(var)
                #if var.immediate:
                #    print(name, 'immediate')

    def import_native_module(self, m, alias=None):
        if not alias:
            alias = m.__name__
            alias = alias.replace(".", "/")
        print(m, alias)
    
        names = dir(m)
        for name in names:
            localname = f'{alias}/{name}'
            val = getattr(m, name)
            #print("setting", localname)
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

    def keys(self):
        return self.contents.keys()

    def __contains__(self, key):
        return self.contents.__contains__(key)

    def __delattr__(self, key):
        return self.contents.__delattr__(key)

    def __setitem__(self, key, x):
        return self.set(key, x)

    def __iter__(self):
        return self.contents.__iter__()

    def __getitem__(self, key):
        return self.contents.__getitem__(key)

    def __str__(self):
        return f'Namespace({self.name})'
