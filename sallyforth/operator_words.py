from util import word

@word('>')
def gt(forth):
    a = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(b > a)

@word('<')
def lt(forth):
    a = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(b < a)

@word('=')
def eq(forth):
    a = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(a==b)

@word('<=')
def le(forth):
    a = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(b<=a)

@word('>=')
def ge(forth):
    a = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(b>=a)

@word('+')
def add(forth):
    a = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(b+a)

@word('*')
def mul(forth):
    a = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(b*a)

@word('-')
def sub(forth):
    a = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(b-a)

@word('/')
def div(forth):
    a = forth.stack.pop()
    b = forth.stack.pop()
    forth.stack.push(b/a)

@word('and')
def w_and(forth):
    forth.stack.push(forth.stack.pop() and forth.stack.pop())

@word('or')
def w_or(forth):
    forth.stack.push(forth.stack.pop() or forth.stack.pop())

@word('not')
def w_not(forth):
    forth.stack.push(not forth.stack.pop())


