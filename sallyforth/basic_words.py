import tokenstream as ts
from wrappers import noop
from namespace import Namespace
from util import word, native_word
from unique import Unique
import python_compiler as pc
import inliner
import importlib
from pprint import pprint

@word()
def compile(forth):
    name = forth.stack.pop()
    var = forth.ns[name]
    word_f = var.value
    new_f = pc.compile_word_f(word_f, name)
    forth.set(name, new_f)

@word()
def inline(forth):
    name = forth.stack.pop()
    var = forth.ns[name]
    word_f = var.value
    new_f = inliner.compile_word_f(word_f, name)
    forth.set(name, new_f)

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

@word("go!")
def exec_word(forth):
    func = forth.stack.pop()
    func(forth)

@word("function")
def function_word(forth):
    name = forth.stack.pop()
    var = forth.ns[name]
    word_f = var.value
    def native_f(*args):
        forth.stack.push(args)
        word_f(forth)
        result = forth.stack.pop()
        return result
    forth.stack.push(native_f)

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
    try:
        result = func(*args)
    except:
        print(f'Error executing {func}({args})')
        raise
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

@word('debug-ns')
def debug_ns(forth):
    print('debug ns')
    print(forth.ns.name)
    pprint(forth.ns.includes)
    pprint(forth.ns.contents)

@word('*ns*')
def star_ns_star(forth):
    forth.stack.push(forth.ns)

@word('new-ns')
def new_ns(forth):
    name = forth.stack.pop()
    core = forth.namespaces['core']
    namespace = Namespace(name, [core])
    forth.namespaces[name] = namespace

@word('include')
def include_ns(forth):
    name = forth.stack.pop()
    included = forth.namespaces[name]
    forth.ns.include_ns(included)

@word('set-ns')
def set_ns_word(forth):
    name = forth.stack.pop()
    forth.set_ns(name)

@word('ns?')
def ns_question(forth):
    name = forth.stack.pop()
    forth.stack.push(name in forth.namespaces)

@word(':', True)
def colon(forth):
    name = forth.stream.get_token().value
    body = forth.compile_next()
    forth.set(name, body)
    forth.core.set_constant('*last-word*', name)
    return noop

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
    #print("cond:", cond)
    #print("body", body)
    def dowhile(xforth):
        b = fresult(xforth, cond)
        while b:
            body(xforth)
            b = fresult(xforth, cond)
    dowhile.operation_type = 'while'
    dowhile.immediate = False
    return dowhile

@word('if', True)
def w_if(forth):
    compiled = forth.compile_next()
    def doif(forth):
        value = forth.stack.pop()
        if value:
            compiled(forth)
    doif.operation_type = 'if'
    doif.immediate = False
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
    doif.operation_type = 'ifelse'
    doif.immediate = False
    return doif
