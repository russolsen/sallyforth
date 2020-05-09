import tokenstream as ts
from wrappers import noop
from util import word
from unique import Unique
import importlib
from pprint import pprint

@word('raise')
def w_raise(f):
    ex = f.stack.pop()
    raise ex

@word(immediate=True)
def readtoken(f):
    t = f.stream.get_token()
    def push_token(xforth):
        xforth.stack.push(t)
    return push_token

@word("!!")
def w_call(f):
    func = f.stack.pop()
    args = f.stack.pop()
    #print('f', f, 'args', args)
    try:
        result = func(*args)
    except:
        print(f'Error executing {func}({args})')
        raise
    #print('result', result)
    f.stack.push(result)

@word()
def unique(f):
    f.stack.push(Unique())

@word()
def load(f):
    name = f.stack.pop()
    m = importlib.import_module(name)
    f.set_constant(name, m)

@word('import')
def w_import(f):
    name = f.stack.pop()
    m = importlib.import_module(name)
    f.ns.import_native_module(m)

@word()
def lexicon(f):
    name = f.stack.pop()
    m = importlib.import_module(name)
    f.ns.import_from_module(m)

@word('source')
def w_source(f):
    path = f.stack.pop()
    f.eval_file(path)

@word('alias')
def w_alias(f):
    new_name = f.stack.pop()
    old_name = f.stack.pop()
    f.alias(new_name, old_name)

@word()
def rawdef(f):
    name = f.stack.pop()
    value = f.stack.pop()
    f.set(name, value)

@word("=!")
def equal_bang(f):
    name = f.stack.pop()
    value = f.stack.pop()
    f.set_constant(name, value)

@word("*prompt*")
def promptword(f):
    f.stack.push(">> ")

@word()
def lookup(f):
    name = f.stack.pop()
    f.stack.push(f.ns[name])

@word()
def forget(f):
    name = f.stack.pop()
    del f.ns[name]

@word()
def p(f):
    print(f.stack.pop())

@word()
def nl(f):
    print()

@word('.')
def dot(f):
    print(f.stack.pop(), end='')

@word()
def splat(f):
    l = f.stack.pop()
    l.reverse()
    for x in l:
        f.stack.push(x)

@word()
def stack(f):
    print(f.stack)

@word()
def ns(f):
    print(f.ns.name)
    print(f.ns.contents)

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
    print("Word name:", name)
    var = forth.ns[name]
    print('var', var)
    print('value', var.value)
    print('value dict', var.value.__dict__)
    var.value.forth_inline = True
    print('moded value dict', var.value.__dict__)

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

@word()
def fresult(forth, f):
    f(forth)
    result = forth.stack.pop()
    return result

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
