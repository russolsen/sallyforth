import sys
from os import path
from words import *
import words
from lex import forth_prompt, read_tokens, is_string, tokenize
from stack import Stack

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
        self.dictionary = {
                '*prompt*': const_f('SallyForth>> '),
                'true': const_f(True),
                'false': const_f(False),
                'nil': const_f(None),
                '0': const_f(0),
                '1': const_f(1),
                '2': const_f(2),
                ';': w_semi,
                ':': w_colon,
                '->list': w_list,
                '[': w_startlist,
                ']': w_endlist,
                '{': w_startmap,
                '}': w_endmap,
                '@@': w_lookup,
                '!!': w_call,
                '+': w_add,
                '+': w_add,
                '-': w_sub,
                '/': w_div,
                '>': w_gt,
                '<': w_lt,
                '<=': w_le,
                '>=': w_ge,
                '=': w_eq,
                '.': w_dot}

        self.import_from_module(words, 'w_')

        self.compiler = None
        if startup:
            execute_startup(startup)

    def import_from_module(self, m, prefix):
        names = dir(m)
        prefix_len = len(prefix)
        for name in names:
            if name.startswith(prefix):
                word_name = name[prefix_len::]
                self.dictionary[word_name] = m.__getattribute__(name)

    def defvar(self, name, value):
        self.dictionary[name] = const_f(value)

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
            if not self.compiling():
                self.execute_token(token)
            else:
                self.compile_token(token)

    def execute_file(self, fpath):
        old_source = self.dictionary.get('*source*', None)
        self.defvar('*source*', fpath)
        with open(fpath) as f:
            line = f.readline()
            while line:
                tokens = tokenize(line)
                self.execute_tokens(tokens)
                line = f.readline()
        self.defvar('*source*', '')
        self.dictionary['*source*'] = old_source

    def compile_token(self, token):
        if self.compiler.name == None:
            self.compiler.name = token
            return

        if is_string(token):
            self.compiler.add_instruction(const_f(token[1::]))
            return

        if token in self.dictionary:
            word = self.dictionary[token]
            if 'immediate' in word.__dict__:
                #print('before immediate word:', self, self.dictionary)
                word(self, 0)
                #print('after immediate word:', self, self.dictionary)
            else:
                self.compiler.add_instruction(self.dictionary[token])
            return

        n = to_number(token)
        if n == None:
            self.compiler = None
            print(f'{token}? Compile terminated.')
        else:
            self.compiler.add_instruction(const_f(n))

    def execute_token(self, token):
        if is_string(token):
            self.stack.push(token[1::])
            return

        if token in self.dictionary:
            self.dictionary[token](self, 0)
            return

        n = to_number(token)
        if n == None:
            print(f'{token}?')
        else:
            self.stack.push(n)

    def dump(self):
        print('Forth:', self)
        print('Stack:', self.stack)
        print('Dictionary:', self.dictionary)
        print('Compiler:', self.compiler)
