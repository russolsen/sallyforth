from compiler import Compiler
import importlib

def execute_f(name, instructions):
    # print("execute_f:", len(instructions))
    def inner(forth, debug=False):
        # print("inner f:", name)
        # print("inner f:", len(instructions))
        i = 0
        while i >= 0:
            # print(i, "=>", instructions[i])
            delta = instructions[i](forth)
            i += delta
        return 1
    return inner

def ifnot_jump_f(n):
    def ifnot_jump(forth):
        # print("If not jump:")
        x = forth.stack.pop()
        # print("==>value:", x)
        if not x:
            # print("==>", x, " is false")
            # print("==>returning", n)
            return n
        # print("==>returning 1")
        return 1
    return ifnot_jump

def const_f(value):
    def x(f):
        f.stack.push(value)
        return 1
    return x

def w_import(f):
    name = f.stack.pop()
    m = importlib.import_module(name)
    f.stack.push(m)

def w_def(f):
    value = f.stack.pop()
    name = f.stack.pop()
    f.defvar(name, value)
    print('name', name, 'value', value)

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
    print("Should not execute this word!")
    raise ValueError

def w_if(forth):
    print("w_if")
    compiler = forth.compiler
    compiler.push_offset()
    compiler.add_instruction(w_should_not_happen)
    return 1

w_if.__dict__['immediate'] = True

def w_then(forth):
    compiler = forth.compiler
    if_offset = compiler.pop_offset()
    end_offset = compiler.offset()
    delta = end_offset - if_offset
    compiler.instructions[if_offset] = ifnot_jump_f(delta)
    return 1

w_then.__dict__['immediate'] = True

def w_do(forth):
    print("w_do")
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
    print("Delta:", delta)
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
    print(f.stack)
    return 1

