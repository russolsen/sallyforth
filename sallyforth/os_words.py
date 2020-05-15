import os
import sys
from util import word

@word('fork')
def w_fork(forth):
    parent_word = forth.stack.pop()
    child_word = forth.stack.pop()
    parent_f = forth.ns.get(parent_word, None).get_ivalue()
    child_f = forth.ns.get(child_word, None).get_ivalue()
    pid = os.fork()
    forth.stack.push(pid)
    if pid == 0:
        print("child:", pid)
        child_f(f, 0)
    else:
        print("parent:", pid)
        parent_f(f, 0)

@word('execvp')
def w_execvp(forth):
    args = forth.stack.pop()
    path = args[0]
    print(f"path {path} args: {args}")
    os.execvp(path, args)

@word('waitpid')
def w_waitpid(forth):
    pid = forth.stack.pop()
    result = os.waitpid(pid, 0)
    forth.stack.push(result)

@word('exit')
def w_exit(forth):
    n = forth.stack.pop()
    sys.exit(n)

@word('exit!')
def w_exit_bang(forth):
    n = forth.stack.pop()
    os._exit(n)
