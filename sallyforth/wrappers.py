def value_f(value):
    def push_constant(f):
        f.stack.push(value)
    push_constant.immediate = False
    push_constant.operation_type = 'pushv'
    push_constant.value = value
    push_constant.__doc__ = value.__doc__
    return push_constant

def inner_f(contents):
    if len(contents) == 0:
        f = noop
    elif len(contents) == 1:
        f = contents[0]
    elif len(contents) == 2:
        f = inner_f2(contents)
    elif len(contents) == 3:
        f = inner_f3(contents)
    else:
        f = inner_fn(contents)

    #print("f", f)
    return f


def inner_fn(contents):
    def i_n(forth):
        #print("inner_fn:", contents)
        for fn in contents:
            fn(forth)
    #print("i_n", i_n)
    i_n.immediate = False
    i_n.operation_type = 'inner'
    i_n.contents = contents
    return i_n

def inner_f2(contents):
    f1 = contents[0]
    f2 = contents[1]
    def i_2(forth):
        #print('inner2:', f1, f2)
        f1(forth)
        f2(forth)
    i_2.immediate = False
    i_2.operation_type = 'inner'
    i_2.contents = contents
    return i_2

def inner_f3(contents):
    f1 = contents[0]
    f2 = contents[1]
    f3 = contents[2]
    def i_3(forth):
        f1(forth)
        f2(forth)
        f3(forth)
    i_3.immediate = False
    i_3.operation_type = 'inner'
    i_3.contents = contents
    return i_3

def noop(value):
    pass
##noop.immediate = False
##noop.operation_type = 'noop'
