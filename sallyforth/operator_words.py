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

def w_and(f, i):
    f.stack.push(f.stack.pop() and f.stack.pop())
    return i+1

def w_or(f, i):
    f.stack.push(f.stack.pop() or f.stack.pop())
    return i+1

def w_not(f, i):
    f.stack.push(not f.stack.pop())
    return i+1


