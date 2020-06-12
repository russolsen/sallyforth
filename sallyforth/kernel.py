import sys
import os
from stack import Stack
from namespace import Namespace
from kword import Keyword
import tokenstream as ts
import threaded_compiler as compiler
from wrappers import value_f

class Forth:
    """
    A class to represent a SallyForth execution context.

    An instance of the Forth class is all you need to execute
    SallyForth code.

    Attributes
    ----------
    stack : Stack
        Data stack used by most every word.
    namespaces : String -> Namespace dictionary
        All of the Forth namespaces indexed by ns name.
    ns : Namespace
        The currently active Namespace.
    core : Namespace
        The core namespace. Has all the Forth built-in words.
    user : Namespace
        The more or less empty default namespace.
    """

    def __init__(self):
        """
        Construct a new SallyForth execution environment.
        """
        self.stack = Stack()
        self.stream = None
        core = Namespace('core')
        user = Namespace('user', [core])
        user.include_ns(core)
        self.namespaces = {}
        self.namespaces[core.name] = core
        self.namespaces[user.name] = user
        self.ns = core
        self.core = core
        self.set_constant('forth', self)
        self.set_constant('nil', None)
        self.set_constant('true', True)
        self.set_constant('false', False)
        self.set_constant('*source*', '<<input>>')
        self.set_constant('*last-word*', None)
        sally_dir = os.path.dirname(os.path.abspath(__file__))
        self.set_constant('*sallyforth-dir*', sally_dir)
        self.ns.import_from_module('basic_words')
        self.ns.import_from_module('namespace_words')
        self.ns.import_from_module('stack_words')
        self.ns.import_from_module('operator_words')
        self.ns.import_from_module('data_words')
        self.eval_file(f'{sally_dir}/0.sf')
        self.ns = user

    def set_constant(self, name, value):
        """
        Sets name in the current namespace to a function that will push value onto the stack.
        """
        return self.ns.set_constant(name, value)

    def set(self, name, fvalue):
        """
        Sets name in the current namespace to the given function.
        """
        return self.ns.set(name, fvalue)

    def get(self, name, def_value=None):
        """
        Get the value associated with name in the current namespace (and it's includes).
        """
        if name in self.ns:
            return self.ns[name]
        return def_value

    def alias(self, new_name, old_name):
        """
        Given an existing value in the current namespace an additional name.
        """
        self.ns.alias(new_name, old_name)

    def set_ns(self, new_ns_name):
        """
        Set the current namespace.
        """
        self.ns = self.namespaces[new_ns_name]

    def compile_next(self, current_token=None):
        """
        Compile the next token, either the one passed in 
        or the next one on the current token stream.
        """
        return compiler.compile_next(self, self.stream, current_token)

    def eval_stream(self, stream):
        """
        Evaluate the contents of the given token stream.
        """
        old_stream = self.stream
        self.stream = stream
        compiler.eval_stream(self, stream)
        self.stream = old_stream

    def eval_file(self, path):
        """
        Evaluate the contents of the given file as Forth source code.
        """
        old_source = self.ns['*source*']
        old_ns = self.ns
        with open(path) as f:
            fns = ts.file_token_stream(f)
            result = self.eval_stream(fns)
            self.ns = old_ns
            self.ns['*source*'] = old_source
            return result

    def eval_string(self, s):
        """
        Evaluate a string as Forth source code.
        """
        self.eval_stream(ts.string_token_stream(s))

    def eval_string_r(self, s):
        """
        Evaluate a string and return the top of the resulting stack.
        """
        self.eval_string(s)
        return self.stack.pop()

    def eval_object(self, o):
        if isinstance(o, [int, str, Keyword, float]):
            self.stack.push(o)
        elif callable(o):
            o(self)
        else:
            print(o, "??")
            raise ValueError()

    def eval_objects(self, l):
        for o in l:
            self.eval_object(l)

    def lookup(self, name):
        """
        Return the value of the given name in the current namespace.
        """
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
