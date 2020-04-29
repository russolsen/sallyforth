from inspect import isfunction, isbuiltin
import importlib
import os
from compiler import Compiler
from arglist import Arglist

def const_f(value):
    def x(f, i):
        #print("const f, pushing", value)
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

def w_nexttoken(f, i):
    token = f.read_next_token()
    f.stack.push(token)
    return i+1

def w_eval(f, i):
    token = f.stack.pop()
    f.execute_token(token)
    return i+1

def w_no_op(f, i):
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

    relative_dir = os.path.dirname(f.evaluate_string('*source*'))
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
            new_j = instructions[j](forth, j)
            if new_j == None:
                print(f'Instruction {instructions[j]} None')
                raise RuntimeError
            j = new_j
        return i + 1
    return inner

def ifnot_jump_f(n):
    def ifnot_jump(forth, i):
        x = forth.stack.pop()
        if not x:
            return i+n
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
    try:
        result = func(*args)
    except:
        print(f'Error executing {func}{list(args)}')
        raise
    # print('result', result)
    f.stack.push(result)
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
    print("Stack:", end=' ')
    for x in f.stack:
        print(f'{repr(x)}', end=' ')
    print()
    return i+1
    
def w_enlist(f, i):
    # print("Enlist!")
    x = f.stack.pop()
    # print("Popped", x)
    f.stack.push([x])
    return i+1


