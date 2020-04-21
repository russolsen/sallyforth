import sys
from os import path
from words import *
import words
from lex import forth_prompt, read_tokens, is_string, tokenize
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
        self.stack = Stack()
        self.namespaces = {}
        initial_defs = {
                '*prompt*': const_f('SallyForth>> '),
                'true': const_f(True),
                'false': const_f(False),
                'nil': const_f(None),
                '0': const_f(0),
                '1': const_f(1),
                '2': const_f(2)}

        self.forth_ns = self.make_namespace('forth', initial_defs)
        user_ns = self.make_namespace('user', {}, [self.forth_ns])

        self.forth_ns.import_from_module(words, 'w_')
        self.namespace = self.forth_ns

        self.compiler = None

        self.defvar("argv", sys.argv[1::])

        if startup:
            self.execute_file(startup)

        self.namespace = user_ns

    def defvar(self, name, value):
        self.namespace[name] = const_f(value)

    def evaluate_token(self, token):
        self.execute_token(token)
        return self.stack.pop()

    def compiling(self):
        return self.compiler

    def execute_line(self, readline_f=forth_prompt):
        tokens = read_tokens(readline_f)
        self.execute_tokens(tokens)

    def execute_tokens(self, tokens):
        for token in tokens:
            # print("token:", token)
            if not self.compiling():
                self.execute_token(token)
            else:
                self.compile_token(token)

    def set_ns(self, ns_name):
        if ns_name in self.namespaces:
            self.namespace = self.namespaces[ns_name]
        else:
            raise ValueError(f'No such namespace: {ns_name}')

    def make_namespace(self, ns_name, initial_defs={}, refers=[]):
        print(f'New namespace {ns_name} {refers}')
        result = Namespace(ns_name, initial_defs, refers)
        self.namespaces[ns_name] = result
        print(f'Returning {result}')
        return result

    def execute_file(self, fpath):
        old_source = self.namespace.get('*source*', None)
        old_namespace = self.namespace
        self.defvar('*source*', fpath)
        with open(fpath) as f:
            line = f.readline()
            while line:
                tokens = tokenize(line)
                self.execute_tokens(tokens)
                line = f.readline()
        self.namespace['*source*'] = old_source
        self.namespace = old_namespace

    def compile_token(self, token):
        if self.compiler.name == None:
            self.compiler.name = token
            return

        if is_string(token):
            self.compiler.add_instruction(const_f(token[1::]))
            return

        if token in self.namespace:
            word = self.namespace[token]
            if 'immediate' in word.__dict__:
                word(self, 0)
            else:
                self.compiler.add_instruction(self.namespace[token])
            return

        n = to_number(token)
        if n == None:
            print(f'{token}? Compile of {self.compiler.name} terminated.')
            self.compiler = None
        else:
            self.compiler.add_instruction(const_f(n))

    def execute_token(self, token):
        # print("x token:", token)
        if is_string(token):
            self.stack.push(token[1::])
            return

        if token in self.namespace:
            self.namespace[token](self, 0)
            return

        n = to_number(token)
        if n == None:
            print(f'{token}?')
        else:
            self.stack.push(n)

    def dump(self):
        print('Forth:', self)
        print('Stack:', self.stack)
        print('Dictionary:', self.namespace)
        print('Compiler:', self.compiler)
