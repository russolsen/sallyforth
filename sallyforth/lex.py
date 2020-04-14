import sys
from os import path

def is_string(token):
    #print("is string:", token, token[0], token[0] == '"')
    return token[0] == '"'

def is_space(ch):
    return ch == " " or ch == "\t" or ch == "\n"

def tokenize(s):
    state = 'start'
    token = ''
    tokens = []
    for ch in s:
        #print(f'Loop state {state} token {token} ch {ch}')
        if state == 'start' and is_space(ch):
            continue
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
        elif state == 'word' and is_space(ch):
            tokens.append(token)
            state = 'start'
            token = ''
        elif state == 'word' or state == 'string':
            token += ch
        else:
            print(f'State: [{state}] token: [{token}] ch: [{ch}]???')
            state = 'start'
    if len(token) > 0:
        tokens.append(token)
    return tokens

def read_ch():
    return sys.stdin.read(1)

def read_tokens(read_f):
    line = read_f()
    return tokenize(line)

def forth_prompt():
    return input("SallyForth>> ")

def file_read_f(f):
    def read_it():
        return f.readline()
    return read_it
