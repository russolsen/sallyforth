from inspect import isfunction, isbuiltin
import importlib
import os
from compiler import Compiler
from arglist import Arglist

class Unique:
    def __str__(self):
        return f'Unique[{id(self)}]'

def const_f(value):
    def x(f, i):
        f.stack.push(value)
        return i + 1
    return x

def native_function_handler(func):
    def handle(forth, i):
        args = forth.stack.pop()
        #print(f"Native fun, calling {func}({args})")
        result = func(*args)
        #print(f'Result: {result}')
        forth.stack.push(result)
        #print("pushed result")
        return i + 1
    return handle

def import_native_module(forth, m, alias=None, excludes=[]):
    if not alias:
        alias = m.__name__
    raw_names = dir(m)
    names = [x for x in raw_names if x not in excludes] 
    for name in names:
        localname = f'{alias}.{name}'
        val = m.__getattribute__(name)
        forth.namespace[localname] = const_f(val)

def w_eval(f, i):
    token = f.stack.pop()
    f.execute_token(token)
    return i+1

def w_no_op(f, i):
    return i+1

def w_enlist(f, i):
    print("Enlist!")
    x = f.stack.pop()
    print("Popped", x)
    f.stack.push([x])
    return i+1

def w_forth(f, i):
    f.stack.push(f)
    return i+1

def w_current_ns(f, i):
    f.stack.push(f.namespace)
    return i + 1

def w_ns(f, i):
    name = f.stack.pop()
    if name in f.namespaces:
        f.namespace = f.namespaces[name]
    else:
        new_ns = f.make_namespace(name, {}, [f.forth_ns])
        f.namespace = new_ns
    return i + 1

def w_alias(f, i):
    new_name = f.stack.pop() 
    old_name = f.stack.pop() 
    f.namespace[new_name] = f.namespace[old_name]
    return i + 1

def w_require(f, i):
    name = f.stack.pop()
    m = importlib.import_module(name)
    import_native_module(f, m, name)
    return i + 1

def source(f, path):
    old_source_f = f.namespace.get('*source*', None)
    old_namespace = f.namespace
    try:
        f.execute_file(path)
    finally:
        f.namespace['*source*'] = old_source_f
        f.namespace = old_namespace

def w_load(f, i):
    path = f.stack.pop()
    source(f, path)
    return i + 1

def w_source(f, i):
    path = f.stack.pop()
    if os.path.isabs(path):
        source(f, path)
        return i+1

    relative_dir = os.path.dirname(f.evaluate_token('*source*'))
    relative_path = f'{relative_dir}/{path}'
    if os.path.exists(relative_path):
        source(f, relative_path)
        return i+1

    source(f, path)
    return i+1


def execute_f(name, instructions):
    #print('execute_f:', name, len(instructions))
    def inner(forth, i, debug=False):
        #print('inner f:', name)
        #print('inner f:', len(instructions))
        j = 0
        while j >= 0:
            #print(j, '=>', instructions[j])
            j = instructions[j](forth, j)
        return i + 1
    return inner

def ifnot_jump_f(n):
    def ifnot_jump(forth, i):
        # print('If not jump:')
        x = forth.stack.pop()
        # print('==>value:', x)
        if not x:
            # print('==>', x, ' is false')
            # print('==>returning', n)
            return i+n
        # print('==>returning 1')
        return i+1
    return ifnot_jump

def jump_f(n):
    def do_jump(forth, i):
        return n+i
    return do_jump

def w_recur(f, i):
    return 0

def w_import(f, i):
    name = f.stack.pop()
    m = importlib.import_module(name)
    f.namespace[name] = const_f(m)
    return i+1

def w_call(f, i):
    func = f.stack.pop()
    args = f.stack.pop()
    # print('f', f, 'args', args)
    result = func(*args)
    # print('result', result)
    f.stack.push(result)
    return i+1

def w_px(f, i):
    args = f.stack.pop()
    name = f.stack.pop()
    m = f.stack.pop()
    func = m.__dict__[name]
    result = func(*args)
    f.stack.push(result)
    return i+1

def w_unique(f, ip):  # pushes a uique object.
    f.stack.push(Unique())
    return ip+1

def w_map(f, ip):
    l = f.stack.pop()
    word = f.stack.pop()

    word_f = f.namespace.get(word, None)
    result = []

    for item in l:
        f.stack.push(item)
        word_f(f, 0)
        result.append(f.stack.pop())

    f.stack.push(result)
    return ip+1

def w_reduce(f, ip):
    l = f.stack.pop()
    word = f.stack.pop()

    word_f = f.namespace.get(word, None)

    if len(l) <= 0:
        f.stack.push(None)
    elif len(l) == 1:
        f.stack.push(l[0])
    else:
        result = l[0]
        l = l[1::-1]
        for item in l:
            f.stack.push(result)
            f.stack.push(item)
            word_f(f, 0)
            result = f.stack.pop()
        f.stack.push(result)

    return ip+1

def w_bounded_list(f, ip):
    """Create a list from delimted values on the stack.
    [list]
    (marker a b c marker -- [a b c]
    """
    marker = f.stack.pop()
    l = []
    x = f.stack.pop()
    while x != marker:
        l.append(x)
        x = f.stack.pop()
    l.reverse()
    f.stack.push(l)
    return ip+1

def w_to_arglist(f, ip):
    l = f.stack.pop()
    f.stack.push(Arglist(l))
    return ip+1

def w_list(f, ip):    # ->list
    n = f.stack.pop()
    l = []
    for i in range(n):
        l.append(f.stack.pop())
    f.stack.push(l)
    return ip+1

def w_thread(f, i):    # @@
    contents = f.stack.pop()
    result = contents[0]
    for field in contents[1::]:
        if isinstance(field, str) and hasattr(result, field):
            result = getattr(result, field)    # result.field
        elif isinstance(field, Arglist):
            result = result(*field)            # result(*field)
        else:
            result = result[field]             # result[field]
    f.stack.push(result)
    return i+1


ListMarker = object()

def w_startlist(f, i):   # [
    f.stack.push(ListMarker)
    return i+1

def w_endlist(f, i):    # ]
    l = []
    x = f.stack.pop()
    while x != ListMarker:
        l.append(x)
        x = f.stack.pop()
    l.reverse()
    f.stack.push(l)
    return i+1

MapMarker = object()

def w_startmap(f, i):   # {
    f.stack.push(MapMarker)
    return i+1

def w_endmap(f, ip):    # }
    l = []
    x = f.stack.pop()
    while x != MapMarker:
        l.append(x)
        x = f.stack.pop()
    if (len(l) % 2) != 0:
        print('Maps need even number of entries.')
        return i+1
    l.reverse()
    result = {}
    for i in range(0, len(l), 2):
        result[l[i]] = l[i+1]
    f.stack.push(result)
    return ip+1

def w_list_to_map(f, ip):  # list->map
    l = f.stack.pop()
    result = {}
    for i in range(0, len(l), 2):
        result[l[i]] = l[i+1]
    f.stack.push(result)
    return ip+1

def w_get(f, i):
    name = f.stack.pop()
    m = f.stack.pop()
    result = m[name]
    f.stack.push(result)
    return i+1

def w_getattribute(f, i):
    name = f.stack.pop()
    x = f.stack.pop()
    result = x.__getattribute__(name)
    f.stack.push(result)
    return i+1

def w_def(f, i):
    value = f.stack.pop()
    name = f.stack.pop()
    f.defvar(name, value)
    print('name', name, 'value', value)
    return i+1

def w_gt(f, i):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b > a)
    return i+1

def w_lt(f, i):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b < a)
    return i+1

def w_eq(f, i):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(a==b)
    return i+1

def w_le(f, i):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b<=a)
    return i+1

def w_ge(f, i):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b>=a)
    return i+1

def w_add(f, i):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b+a)
    return i+1

def w_mul(f, i):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b*a)
    return i+1

def w_sub(f, i):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b-a)
    return i+1

def w_div(f, i):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b/a)
    return i+1

def w_reset(f, i):
    a = f.stack.reset()
    return i+1

def w_dot(f, i):
    a = f.stack.pop()
    print(a, end='')
    return i+1

def w_dup(f, i):
    x = f.stack.peek()
    f.stack.push(x)
    return i+1

def w_tmb(f, i):  # A noop
    # t = f.stack.pop()
    # m = f.stack.pop()
    # b = f.stack.pop()
    # f.stack.push(b)
    # f.stack.push(m)
    # f.stack.push(t)
    return i+1

def w_tbm(f, i):
    t = f.stack.pop()
    m = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(m)
    f.stack.push(b)
    f.stack.push(t)
    return i+1

def w_bmt(f, i):
    t = f.stack.pop()
    m = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(t)
    f.stack.push(m)
    f.stack.push(b)
    return i+1

def w_btm(f, i):
    t = f.stack.pop()
    m = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(m)
    f.stack.push(t)
    f.stack.push(b)
    return i+1

def w_mtb(f, i):
    t = f.stack.pop()
    m = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b)
    f.stack.push(t)
    f.stack.push(m)
    return i+1

def w_mbt(f, i):
    t = f.stack.pop()
    m = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(t)
    f.stack.push(b)
    f.stack.push(m)
    return i+1

def w_rot(f, i):
    c = f.stack.pop()
    b = f.stack.pop()
    a = f.stack.pop()
    f.stack.push(b)
    f.stack.push(c)
    f.stack.push(a)
    return i+1

def w_drop(f, i):
    f.stack.pop()
    return i+1

def w_swap(f, i):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(a)
    f.stack.push(b)
    return i+1

def w_nl(f, i):
    print()
    return i+1

def w_return(f, i):
    return -9999;

def w_colon(f, i):
    f.compiler = Compiler()

def w_semi(forth, i):
    forth.compiler.add_instruction(w_return)
    name = forth.compiler.name
    word_f = execute_f(name, forth.compiler.instructions)
    forth.namespace[name] = word_f
    forth.compiler = None
    return i+1

w_semi.__dict__['immediate'] = True

def w_should_not_happen(forth, i):
    print('Should not execute this word!')
    raise ValueError

def w_if(forth, i):
    #print('w_if')
    compiler = forth.compiler
    compiler.push_offset()
    compiler.push_offset()
    compiler.add_instruction(w_should_not_happen)
    return i+1

w_if.__dict__['immediate'] = True

def w_then(forth, i):
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
    return i+1

w_then.__dict__['immediate'] = True


def w_else(forth, i):
    compiler = forth.compiler
    compiler.pop_offset()
    compiler.push_offset()
    compiler.add_instruction(w_should_not_happen)
    return i+1

w_else.__dict__['immediate'] = True

def w_do(forth, i):
    #print('w_do')
    compiler = forth.compiler
    compiler.push_offset()
    compiler.add_instruction(w_should_not_happen)
    return i+1

w_do.__dict__['immediate'] = True

def w_while(forth, i):
    compiler = forth.compiler
    do_offset = compiler.pop_offset()
    while_offset = compiler.offset()
    delta = do_offset - while_offset
    compiler.instructions[if_offset] = ifnot_jump_f(delta)
    return i+1

w_while.__dict__['immediate'] = True

def w_begin(forth, i):
    compiler = forth.compiler
    compiler.push_offset()
    return i+1

w_begin.__dict__['immediate'] = True

def w_until(forth, i):
    compiler = forth.compiler
    begin_offset = compiler.pop_offset()
    until_offset = compiler.offset()
    delta = begin_offset - until_offset
    #print('Delta:', delta)
    compiler.instructions.append(ifnot_jump_f(delta))
    return i+1


w_until.__dict__['immediate'] = True


def w_dump(f, i):
    f.dump()
    return i+1

def w_idump(f, i):
    f.dump()
    return i+1

w_idump.__dict__['immediate'] = True

def w_stack(f, i):
    print("::top::")
    for x in f.stack:
        print(f'{x}')
    print("::bottom::")
    return i+1
