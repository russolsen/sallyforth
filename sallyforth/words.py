from compiler import Compiler
import importlib
from inspect import isfunction, isbuiltin

def const_f(value):
    def x(f):
        f.stack.push(value)
        return 1
    return x

def native_function_handler(func):
    def handle(forth):
        args = forth.stack.pop()
        result = func(*args)
        forth.stack.push(result)
        return 1
    return handle

def import_native_module(forth, m, alias=None, excludes=[]):
    if not alias:
        alias = m.__name__
    raw_names = dir(m)
    names = [x for x in raw_names if x not in excludes] 
    for name in names:
        localname = f'{alias}.{name}'
        #print(localname)
        val = m.__getattribute__(name)
        if isfunction(val) or isbuiltin(val):
            forth.dictionary[localname] = native_function_handler(val)
        else:
            forth.dictionary[localname] = const_f(val)

def w_require(f):
    name = f.stack.pop()
    m = importlib.import_module(name)
    import_native_module(f, m, name)
    return 1

def w_source(f):
    path = f.stack.pop()
    f.execute_file(path)
    return 1

def execute_f(name, instructions):
    # print('execute_f:', len(instructions))
    def inner(forth, debug=False):
        # print('inner f:', name)
        # print('inner f:', len(instructions))
        i = 0
        while i >= 0:
            # print(i, '=>', instructions[i])
            delta = instructions[i](forth)
            i += delta
        return 1
    return inner

def ifnot_jump_f(n):
    def ifnot_jump(forth):
        # print('If not jump:')
        x = forth.stack.pop()
        # print('==>value:', x)
        if not x:
            # print('==>', x, ' is false')
            # print('==>returning', n)
            return n
        # print('==>returning 1')
        return 1
    return ifnot_jump

def jump_f(n):
    def do_jump(forth):
        return n
    return do_jump

def w_import(f):
    name = f.stack.pop()
    m = importlib.import_module(name)
    f.dictionary[name] = const_f(m)
    return 1

def w_px(f):
    args = f.stack.pop()
    #print('args', args)
    name = f.stack.pop()
    #print('name', name)
    m = f.stack.pop()
    #print('mod:', m)
    func = m.__dict__[name]
    #print('f:', f);
    result = func(*args)
    #print('result', result)
    f.stack.push(result)
    return 1

def w_list(f):
    n = f.stack.pop()
    l = []
    for i in range(n):
        l.append(f.stack.pop())
    #print(l)
    f.stack.push(l)
    return 1

ListMarker = object()

def w_startlist(f):   # [
    f.stack.push(ListMarker)
    return 1

def w_endlist(f):    # ]
    l = []
    x = f.stack.pop()
    while x != ListMarker:
        l.append(x)
        x = f.stack.pop()
    l.reverse()
    f.stack.push(l)
    return 1

MapMarker = object()

def w_startmap(f):   # {
    f.stack.push(MapMarker)
    return 1

def w_endmap(f):    # }
    l = []
    x = f.stack.pop()
    while x != MapMarker:
        l.append(x)
        x = f.stack.pop()
    if (len(l) % 2) != 0:
        print('Maps need even number of entries.')
        return 1
    l.reverse()
    result = {}
    for i in range(0, len(l), 2):
        result[l[i]] = l[i+1]
    f.stack.push(result)
    return 1

def w_get(f):
    name = f.stack.pop()
    m = f.stack.pop()
    result = m[name]
    f.stack.push(result)
    return 1

def w_getattribute(f):
    name = f.stack.pop()
    x = f.stack.pop()
    result = x.__getattribute__(name)
    f.stack.push(result)
    return 1

def w_def(f):
    value = f.stack.pop()
    name = f.stack.pop()
    f.defvar(name, value)
    #print('name', name, 'value', value)
    return 1

def w_gt(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b > a)
    return 1

def w_lt(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b < a)
    return 1

def w_eq(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(a==b)
    return 1

def w_le(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b<=a)
    return 1

def w_ge(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b>=a)
    return 1

def w_add(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b+a)
    return 1

def w_mul(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b*a)
    return 1

def w_sub(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b-a)
    return 1

def w_div(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b/a)
    return 1

def w_dot(f):
    a = f.stack.pop()
    print(a, end='')
    return 1

def w_dup(f):
    x = f.stack.peek()
    f.stack.push(x)
    return 1

def w_rot(f):
    c = f.stack.pop()
    b = f.stack.pop()
    a = f.stack.pop()
    f.stack.push(b)
    f.stack.push(c)
    f.stack.push(a)
    return 1

def w_drop(f):
    f.stack.pop()
    return 1

def w_swap(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(a)
    f.stack.push(b)
    return 1

def w_nl(f):
    print()
    return 1

def w_return(f):
    return -9999999999

def w_colon(f):
    f.compiler = Compiler()

def w_semi(forth):
    forth.compiler.add_instruction(w_return)
    name = forth.compiler.name
    word_f = execute_f(name, forth.compiler.instructions)
    forth.dictionary[name] = word_f
    forth.compiler = None
    return 1

w_semi.__dict__['immediate'] = True

def w_should_not_happen(forth):
    print('Should not execute this word!')
    raise ValueError

def w_if(forth):
    #print('w_if')
    compiler = forth.compiler
    compiler.push_offset()
    compiler.push_offset()
    compiler.add_instruction(w_should_not_happen)
    return 1

w_if.__dict__['immediate'] = True

def w_then(forth):
    compiler = forth.compiler
    else_offset = compiler.pop_offset()
    if_offset = compiler.pop_offset()
    then_offset = compiler.offset()
    if else_offset == if_offset:
        delta = then_offset - if_offset
        compiler.instructions[if_offset] = ifnot_jump_f(delta)
    else:
        if_delta = else_offset - if_offset + 1
        compiler.instructions[if_offset] = ifnot_jump_f(if_delta)
        else_delta = then_offset - else_offset
        compiler.instructions[else_offset] = jump_f(else_delta)
    return 1

w_then.__dict__['immediate'] = True


def w_else(forth):
    compiler = forth.compiler
    compiler.pop_offset()
    compiler.push_offset()
    compiler.add_instruction(w_should_not_happen)
    return 1

w_else.__dict__['immediate'] = True

def w_do(forth):
    #print('w_do')
    compiler = forth.compiler
    compiler.push_offset()
    compiler.add_instruction(w_should_not_happen)
    return 1

w_do.__dict__['immediate'] = True

def w_while(forth):
    compiler = forth.compiler
    do_offset = compiler.pop_offset()
    while_offset = compiler.offset()
    delta = do_offset - while_offset
    compiler.instructions[if_offset] = ifnot_jump_f(delta)
    return 1

w_while.__dict__['immediate'] = True

def w_begin(forth):
    compiler = forth.compiler
    compiler.push_offset()
    return 1

w_begin.__dict__['immediate'] = True

def w_until(forth):
    compiler = forth.compiler
    begin_offset = compiler.pop_offset()
    until_offset = compiler.offset()
    delta = begin_offset - until_offset
    #print('Delta:', delta)
    compiler.instructions.append(ifnot_jump_f(delta))
    return 1


w_until.__dict__['immediate'] = True


def w_dump(f):
    f.dump()
    return 1

def w_idump(f):
    f.dump()
    return 1

w_idump.__dict__['immediate'] = True

def w_stack(f):
    print(f'Stack: <B[{f.stack}]T>')
    return 1
