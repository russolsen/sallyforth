import os
import sys
from util import word

@word('fork')
def w_fork(f):
    parent_word = f.stack.pop()
    child_word = f.stack.pop()
    parent_f = f.namespace.get(parent_word, None).get_ivalue()
    child_f = f.namespace.get(child_word, None).get_ivalue()
    pid = os.fork()
    f.stack.push(pid)
    if pid == 0:
        print("child:", pid)
        child_f(f, 0)
    else:
        print("parent:", pid)
        parent_f(f, 0)

@word('execvp')
def w_execvp(f):
    args = f.stack.pop()
    path = args[0]
    print(f"path {path} args: {args}")
    os.execvp(path, args)

@word('waitpid')
def w_waitpid(f):
    pid = f.stack.pop()
    result = os.waitpid(pid, 0)
    f.stack.push(result)

@word('exit')
def w_exit(f):
    n = f.stack.pop()
    sys.exit(n)

@word('exit!')
def w_exit_bang(f):
    n = f.stack.pop()
    os._exit(n)
