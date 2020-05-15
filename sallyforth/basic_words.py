import tokenstream as ts
from wrappers import noop
from util import word, native_word
from unique import Unique
import importlib
from pprint import pprint

@word()
def dynamic(forth):
    name = forth.stack.pop()
    isdyn = forth.stack.pop()
    var = forth.ns[name]
    var.dynamic = isdyn

@word()
def native(forth):
    has_return = forth.stack.pop()
    n = forth.stack.pop()
    native_f = forth.stack.pop()
    name = forth.stack.pop()
    print('has_return', has_return)
    print('n', n)
    print('native_f', native_f)
    print('name', name)
    wrapped_f = native_word(native_f, name, n, has_return)
    forth.set(name, wrapped_f)

@word('raise')
def w_raise(forth):
    ex = forth.stack.pop()
    raise ex

@word(immediate=True)
def readtoken(forth):
    t = forth.stream.get_token()
    def push_token(xforth):
        xforth.stack.push(t)
    return push_token

@word("!!")
def w_call(forth):
    func = forth.stack.pop()
    args = forth.stack.pop()
    #print('f', f, 'args', args)
    try:
        result = func(*args)
    except:
        print(f'Error executing {func}({args})')
        raise
    #print('result', result)
    forth.stack.push(result)

@word()
def unique(forth):
    forth.stack.push(Unique())

@word()
def load(forth):
    name = forth.stack.pop()
    m = importlib.import_module(name)
    forth.set_constant(name, m)

@word('import')
def w_import(forth):
    name = forth.stack.pop()
    m = importlib.import_module(name)
    forth.ns.import_native_module(m)

@word()
def lexicon(forth):
    name = forth.stack.pop()
    forth.ns.import_from_module(name)

@word('source')
def w_source(forth):
    path = forth.stack.pop()
    forth.eval_file(path)

@word('alias')
def w_alias(forth):
    new_name = forth.stack.pop()
    old_name = forth.stack.pop()
    forth.alias(new_name, old_name)

@word()
def rawdef(forth):
    name = forth.stack.pop()
    value = forth.stack.pop()
    forth.set(name, value)

@word("=!")
def equal_bang(forth):
    name = forth.stack.pop()
    value = forth.stack.pop()
    forth.set_constant(name, value)

@word("*prompt*")
def promptword(forth):
    forth.stack.push(">> ")

@word()
def lookup(forth):
    name = forth.stack.pop()
    forth.stack.push(forth.ns[name])

@word()
def forget(forth):
    name = forth.stack.pop()
    del forth.ns[name]

@word()
def p(forth):
    print(forth.stack.pop())

@word()
def nl(forth):
    print()

@word('.')
def dot(forth):
    print(forth.stack.pop(), end='')

@word()
def splat(forth):
    l = forth.stack.pop()
    l.reverse()
    for x in l:
        forth.stack.push(x)

@word()
def stack(forth):
    print(forth.stack)

@word()
def ns(forth):
    print(forth.ns.name)
    print(forth.ns.contents)

@word(':', True)
def colon(forth):
    name = forth.stream.get_token().value
    body = forth.compile_next()
    forth.set(name, body)
    forth.set_constant('*last-word*', name)
    return noop

@word()
def inline(forth):
    name = forth.stack.pop()
    var = forth.ns[name]
    value = var.value
    if not value.forth_primitive:
        value.forth_inline = True

@word()
def current_stream(forth):
    forth.stack.push(forth.stream)

@word()
def debug(forth):
    word = forth.stack.pop()
    print("Word:", word)
    var = forth.ns[word]
    pprint(var)
    pprint(var.value.__dict__)

def fresult(forth, f):
    f(forth)
    result = forth.stack.pop()
    return result

@word()
def compilenext(forth):
    forth.stack.push(forth.compile_next())

@word('word!')
def word_bang(forth):
    f = forth.stack.pop()
    f(forth)

@word('while', True)
def w_while(forth):
    cond = forth.compile_next()
    body = forth.compile_next()
    def dowhile(xforth):
        b = fresult(xforth, cond)
        while b:
            body(xforth)
            b = fresult(xforth, cond)
    dowhile.forth_inline = False
    dowhile.forth_primitive = True
    dowhile.forth_immediate = False
    return dowhile

@word('if', True)
def w_if(forth):
    compiled = forth.compile_next()
    print("compiled", compiled)
    def doif(forth):
        value = forth.stack.pop()
        if value:
            compiled(forth)
    doif.forth_inline = False
    doif.forth_primitive = True
    doif.forth_immediate = False
    return doif

@word('ifelse', True)
def ifelse(forth):
    compiled_true = forth.compile_next()
    compiled_false = forth.compile_next()
    def doif(forth):
        value = forth.stack.pop()
        if value:
            compiled_true(forth)
        else:
            compiled_false(forth)
    doif.forth_inline = False
    doif.forth_primitive = True
    doif.forth_immediate = False
    return doif
