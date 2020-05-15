import sys
import os
from stack import Stack
from namespace import Namespace
#import basic_words
#import stack_words
#import operator_words
#import data_words
import tokenstream as ts
import compiler
from wrappers import value_f

class Forth:
    def __init__(self):
        self.stack = Stack()
        self.stream = None
        self.ns = Namespace('core')
        self.set_constant('forth', self)
        self.set_constant('nil', None)
        self.set_constant('true', True)
        self.set_constant('false', False)
        self.set_constant('*source*', '<<input>>')
        self.set_constant('*last-word*', None)
        self.set_constant('*sallyforth-dir*',
                os.path.dirname(os.path.abspath(__file__)))
        self.ns.import_from_module('basic_words')
        self.ns.import_from_module('stack_words')
        self.ns.import_from_module('operator_words')
        self.ns.import_from_module('data_words')

    def set_constant(self, name, value):
        return self.ns.set(name, value_f(value))

    def set(self, name, fvalue):
        return self.ns.set(name, fvalue)

    def get(self, name, def_value=None):
        if name in self.ns:
            return self.ns[name]
        return def_value

    def alias(self, new_name, old_name):
        self.ns.alias(new_name, old_name)

    def compile_next(self, current_token=None):
        return compiler.compile_next(self, self.stream, current_token)

    def eval_stream(self, stream):
        old_stream = self.stream
        self.stream = stream
        compiler.eval_stream(self, stream)
        self.stream = old_stream

    def eval_file(self, path):
        old_source = self.ns['*source*']
        with open(path) as f:
            fns = ts.file_token_stream(f)
            return self.eval_stream(fns)
        self.ns['*source*'] = old_source

    def eval_string(self, s):
        self.eval_stream(ts.string_token_stream(s))

    def eval_string_r(self, s):
        self.eval_string(s)
        return self.stack.pop()

    def lookup(self, name):
        return self.ns[name]

if __name__ == "__main__":
    x = 0
    
    def pmt():
        global x
        x += 1
        return f'Yes{x}>> '
    
    pis = ts.PromptInputStream(pmt)
    tstream = ts.TokenStream(pis.getc)
    
    forth = Forth()
    forth.eval_stream(tstream)
