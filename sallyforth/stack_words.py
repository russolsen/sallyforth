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
def swap(forth):
    a = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(a)
    forth.stack.push(b)
 
@word()
def t(forth):
    dup(forth)

@word()
def m(forth):
    forth.stack.push(forth.stack[-2])

@word()
def b(forth):
    forth.stack.push(forth.stack[-3])

@word()
def tmb(forth):  # A noop
    pass

@word()
def tbm(forth):
    t = forth.stack.pop()
    m = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(m)
    forth.stack.push(b)
    forth.stack.push(t)

@word()
def bmt(forth):
    t = forth.stack.pop()
    m = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(t)
    forth.stack.push(m)
    forth.stack.push(b)

@word()
def btm(forth):
    t = forth.stack.pop()
    m = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(m)
    forth.stack.push(t)
    forth.stack.push(b)

@word()
def mtb(forth):
    t = forth.stack.pop()
    m = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(b)
    forth.stack.push(t)
    forth.stack.push(m)

@word()
def mbt(forth):
    t = forth.stack.pop()
    m = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(t)
    forth.stack.push(b)
    forth.stack.push(m)

@word()
def rot(forth):
    c = forth.stack.pop()
    b = forth.stack.pop()
    a = forth.stack.pop()
    forth.stack.push(b)
    forth.stack.push(c)
    forth.stack.push(a)
