import sys
from os import path
from words import *
from lex import forth_prompt, read_tokens, is_string
from stack import Stack

def to_number(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return None

def push_value_f(value):
    def x(f):
        f.stack.push(value)
        return 1
    return x

class Forth:
    def __init__(self, startup=None):
        self.stack = Stack()
        self.dictionary = {
                'true': const_f(True),
                'false': const_f(False),
                'nil': const_f(None),
                '0': const_f(0),
                '1': const_f(1),
                '2': const_f(2),
                ';': w_semi,
                ':': w_colon,
                '+': w_add,
                '+': w_add,
                '-': w_sub,
                '/': w_div,
                '>': w_gt,
                '<': w_lt,
                '<=': w_le,
                '>=': w_ge,
                '=': w_eq,
                'dup': w_dup,
                'swap': w_swap,
                '.': w_dot,
                'nl': w_nl,
                'dump': w_dump,
                'idump': w_idump,
                'stack': w_stack,
                'begin': w_begin,
                'until': w_until,
                'if': w_if,
                'then': w_then}

        self.compiler = None
        if startup:
            execute_startup(startup)

    def compiling(self):
        return self.compiler

    def process_line(self, readline_f=forth_prompt):
        tokens = read_tokens(readline_f)
        for token in tokens:
            if not self.compiling():
                self.interpret_token(token)
            else:
                self.compile_token(token)

    def compile_token(self, token):
        if self.compiler.name == None:
            self.compiler.name = token
            return

        if is_string(token):
            self.compiler.add_instruction(push_value_f(token[1::]))
            return

        if token in self.dictionary:
            word = self.dictionary[token]
            if 'immediate' in word.__dict__:
                #print("before immediate word:", self, self.dictionary)
                word(self)
                #print("after immediate word:", self, self.dictionary)
            else:
                self.compiler.add_instruction(self.dictionary[token])
            return

        n = to_number(token)
        if n == None:
            self.compiler = None
            print(token, "? Compile terminated.")
        else:
            self.compiler.add_instruction(push_value_f(n))

    def interpret_token(self, token):
        if is_string(token):
            self.stack.push(token)
            return

        if token in self.dictionary:
            self.dictionary[token](self)
            return

        n = to_number(token)
        if n == None:
            print(token, "?")
        else:
            self.stack.push(n)

    def dump(self):
        print("Forth:", self)
        print("Stack:", self.stack)
        print("Dictionary:", self.dictionary)
        print("Compiler:", self.compiler)
