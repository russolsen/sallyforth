def w_px(f, i):
    args = f.stack.pop()
    name = f.stack.pop()
    m = f.stack.pop()
    func = m.__dict__[name]
    result = func(*args)
    f.stack.push(result)
    return i+1

def w_reset(f, i):
    a = f.stack.reset()
    return i+1

def w_dot(f, i):
    a = f.stack.pop()
    print(a, end='')
    return i+1

def w_splat(f, i):
    l = f.stack.pop()
    l.reverse()
    for x in l:
        f.stack.push(x)
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
