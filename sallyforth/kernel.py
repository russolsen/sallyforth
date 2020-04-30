import sys
from os import path
import basic_words, data_words, operator_words, stack_words, os_words
from basic_words import const_f, w_enlist
import tokenstream as ts
from stack import Stack
from namespace import Namespace

def to_number(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return None

class Forth:
    def __init__(self, startup=None):
        self.streams = Stack()
        self.stack = Stack()
        self.namespaces = {}

        self.forth_ns = self.make_namespace('forth')
        self.namespace = self.forth_ns
        user_ns = self.make_namespace('user', {}, [self.forth_ns])

        self.defword('*prompt*', const_f('SallyForth>> '))
        self.defword('*source*', const_f(__file__))
        self.defword('true', const_f(True))
        self.defword('false', const_f(False))
        self.defword('None', const_f(None))
        self.defword('0', const_f(0))
        self.defword('1', const_f(1))
        self.defword('2', const_f(2))

        self.forth_ns.import_from_module(basic_words)
        self.forth_ns.import_from_module(data_words)
        self.forth_ns.import_from_module(operator_words)
        self.forth_ns.import_from_module(stack_words)
        self.forth_ns.import_from_module(os_words)

        self.compiler = None

        self.defvar("argv", sys.argv[1::])

        if startup:
            self.execute_file(startup)

        self.namespace = user_ns

    def defword(self, name, value):
        self.namespace.set(name, value)

    def defvar(self, name, value):
        self.defword(name, const_f(value))

    def compiling(self):
        return self.compiler

    def _compile_token(self, kind, token):
        #print(f"compile: {self.compiler.name}: {token}")
        if self.compiler.name == None:
            print(f'Compiling {token}')
            self.compiler.name = token
            return

        if kind in ['dqstring', 'sqstring']:
            self.compiler.add_instruction(const_f(token))
            return

        if token in self.namespace:
            entry = self.namespace[token]
            #print(token, entry)
            if entry.immediate:
                value = entry.get_ivalue()
                value(self, 0)
            else:
                value = entry.get_cvalue()
                self.compiler.add_instruction(value)
            return

        n = to_number(token)
        if n == None:
            print(f'{token}? Compile of {self.compiler.name} terminated.')
            self.compiler = None
        else:
            self.compiler.add_instruction(const_f(n))

    def _eval_token(self, kind, token):
        if kind in ['dqstring', 'sqstring']:
            self.stack.push(token)
            return

        if token in self.namespace:
            #print("executing ", token)
            f = self.namespace[token].get_ivalue()
            #print(f)
            f(self, 0)
            return

        n = to_number(token)
        if n == None:
            print(f'{token}?')
        else:
            self.stack.push(n)

    def execute_token(self, kind, token):
        #print(f'execute_token: {token}')
        kts = self.macro_expand_token(kind, token)
        #print(kts)
        for kt in kts:
            this_kind, this_token = kt
            if not self.compiling():
                #print("interactive", this_token)
                self._eval_token(this_kind, this_token)
            else:
                #print("compiling...", this_token)
                self._compile_token(this_kind, this_token)
        #print("Done")

    def execute_current_stream(self):
        s = self.streams.peek()
        #print("exec current s:", s)
        kind, token = s.get_token()
        while kind != 'eof':
            self.execute_token(kind, token)
            kind, token = s.get_token()
        self.streams.pop()

    def execute_token_stream(self, s):
        #print("exec token stream:", s)
        self.streams.push(s)
        self.execute_current_stream()

    def execute_string(self, s):
        token_stream = ts.string_token_stream(s)
        return self.execute_token_stream(token_stream)

    def evaluate_string(self, s):
        self.execute_string(s)
        return self.stack.pop()

    def read_next_token(self):
        s = self.streams.peek()
        return s.get_token()

    def py_evaluate(self, s, *args):
        #print(f'Evaluate: token [{token}] args <<{args}>>')
        rargs = list(args)
        rargs.reverse()
        if rargs:
            for a in rargs:
                # print("pushing", a);
                self.stack.push(a)
        print(f'Before eval stack is {str(self.stack)}')
        return self.evaluate_string(s)


    def macro_expand_token(self, kind, token):
        if len(token) <= 0 or token[0] != '#':
            return [[kind, token]]

        tag = token[1:]
        parts = tag.split('.')
        result = [ '<.', parts[0] ]
        result = [['word', '<.'], ['word', parts[0]]]
        for part in parts[1::]:
            result.append(['sqstring', part])
        result.append(['word', '.>'])
        print(result)
        return result

    def set_ns(self, ns_name):
        if ns_name in self.namespaces:
            self.namespace = self.namespaces[ns_name]
        else:
            raise ValueError(f'No such namespace: {ns_name}')

    def make_namespace(self, ns_name, initial_defs={}, refers=[]):
        #print(f'New namespace {ns_name} {refers}')
        result = Namespace(ns_name, initial_defs, refers)
        self.namespaces[ns_name] = result
        #print(f'Returning {result}')
        return result

    def execute_file(self, fpath):
        old_source = self.namespace.get('*source*', None)
        old_namespace = self.namespace
        self.defvar('*source*', fpath)
        with open(fpath) as f:
            fts = ts.file_token_stream(f)
            self.execute_token_stream(fts)
        self.namespace['*source*'] = old_source
        self.namespace = old_namespace

    def dump(self):
        print('Forth:', self)
        print('Stack:', self.stack)
        print('Dictionary:', self.namespace)
        print('Compiler:', self.compiler)
