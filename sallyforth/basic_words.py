from util import word
from unique import Unique
from pprint import pprint

@word("!", doc='Execute the word from the stack: word -- <results>')
def exec_word(forth):
    func = forth.stack.pop()
    func(forth)

@word('raise')
def w_raise(forth):
    ex = forth.stack.pop()
    raise ex

@word("!!", doc='Execute a raw function from the stack: func -- <results>')
def w_call(forth):
    func = forth.stack.pop()
    args = forth.stack.pop()
    try:
        result = func(*args)
    except:
        print(f'Error executing {func}({args})')
        raise
    forth.stack.push(result)

@word(doc='Push a new unique value onto the stack: -- unique')
def unique(forth):
    forth.stack.push(Unique())

@word("*prompt*")
def promptword(forth):
    forth.stack.push(">> ")

@word()
def p(forth):
    print(forth.stack.pop())

@word(doc='Print a newline: - ')
def nl(forth):
    print()

@word('.', doc='Print the value on top of the stack: v --')
def dot(forth):
    print(forth.stack.pop(), end='')

@word()
def splat(forth, doc='Pop a collection and push each item separately: col -- col[n]..col[0]'):
    l = forth.stack.pop()
    l.reverse()
    for x in l:
        forth.stack.push(x)

@word(doc='Print the stack: --')
def stack(forth):
    print(forth.stack)

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
