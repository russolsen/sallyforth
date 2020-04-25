import sys
import readline
from os import path

def is_string(token):
    return token[0] == '"' or token[0] == "'"

def is_space(ch):
    return ch == ' ' or ch == '\t' or ch == '\n'

class Tokenizer:
    def __init__(self, forth):
        self.forth = forth

    def tokenize(self, s):
        raw_tokens = self.raw_tokenize(s)
        return self.forth.macro_expand_tokens(raw_tokens)

    def raw_tokenize(self, s):
        state = 'start'
        token = ''
        tokens = []
        for ch in s:
            #print(f'Loop state {state} token {token} ch {ch}')
            if state == 'start' and ch == '(':
                state = 'comment'
            elif state == 'start' and ch == '\\':
                state = 'line_comment'
            elif state == 'line_comment' and ch == '\n':
                state = 'start'
            elif state == 'comment' and ch == ')':
                state = 'start'
            elif state in ['comment', 'line_comment']:
                continue
            elif state == 'start' and is_space(ch):
                continue
            elif state == 'start' and ch == "'":
                token = ch
                state = 's_string'
            elif state == 'start' and ch == '"':
                token = ch
                state = 'string'
            elif state == 'start':
                token = ch
                state = 'word'
            elif state == 'string' and ch == '"':
                tokens.append(token)
                state = 'start'
                token = ''
            elif (state in ['word', 's_string']) and is_space(ch):
                tokens.append(token)
                state = 'start'
                token = ''
            elif state == 'word' or state == 'string' or state == 's_string':
                token += ch
            else:
                print(f'State: [{state}] token: [{token}] ch: [{ch}]???')
                state = 'start'
        if len(token) > 0:
            tokens.append(token)
        return tokens
