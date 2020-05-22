def value_f(value):
    def push_constant(f):
        f.stack.push(value)
    push_constant.forth_inline = False
    push_constant.forth_primitive = True
    push_constant.forth_name = 'pushv'
    push_constant.forth_immediate = False
    return push_constant

def inner_f(contents):
    def inner(forth):
        for fn in contents:
            fn(forth)
    inner.forth_primitive = False
    inner.forth_immediate = False
    inner.forth_contents = contents
    inner.forth_inline = False
    return inner

def inner2_f(f1, f2):
    def inner2(forth):
        #print('inner2:', f1, f2)
        f1(forth)
        f2(forth)
    inner2.forth_primitive = False
    inner2.forth_contents = [f1, f2]
    inner2.forth_primitive = True
    inner2.forth_immediate = False
    inner2.forth_inline = False
    return inner2

def inner3_f(f1, f2, f3):
    def inner3(forth):
        f1(forth)
        f2(forth)
        f3(forth)
    inner3.forth_primitive = False
    inner3.forth_contents = [f1, f2, f3]
    inner3.forth_immediate = False
    inner3.forth_inline = False
    return inner3

def noop(value):
    pass
noop.forth_inline = False
noop.forth_primitive = True
noop.forth_immediate = False
 

