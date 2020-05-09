from util import word

@word()
def stackdepth(forth):
    forth.stack.push(forth.stack.depth())

@word()
def reset(forth):
    forth.stack.reset()

@word()
def drop(forth):
    forth.stack.pop()

@word()
def dup(forth):
    a = forth.stack.peek()
    forth.stack.push(a)

@word()
def swap(f):
    a = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(a)
    f.stack.push(b)
 
@word()
def tmb(f):  # A noop
    pass

@word()
def tbm(f):
    t = f.stack.pop()
    m = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(m)
    f.stack.push(b)
    f.stack.push(t)

@word()
def bmt(f):
    t = f.stack.pop()
    m = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(t)
    f.stack.push(m)
    f.stack.push(b)

@word()
def btm(f):
    t = f.stack.pop()
    m = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(m)
    f.stack.push(t)
    f.stack.push(b)

@word()
def mtb(f):
    t = f.stack.pop()
    m = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(b)
    f.stack.push(t)
    f.stack.push(m)

@word()
def mbt(f):
    t = f.stack.pop()
    m = f.stack.pop()
    b = f.stack.pop()
    f.stack.push(t)
    f.stack.push(b)
    f.stack.push(m)

@word()
def rot(f):
    c = f.stack.pop()
    b = f.stack.pop()
    a = f.stack.pop()
    f.stack.push(b)
    f.stack.push(c)
    f.stack.push(a)
