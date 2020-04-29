import os
import sys

def w_fork(f, i):
    parent_word = f.stack.pop()
    child_word = f.stack.pop()
    parent_f = f.namespace.get(parent_word, None)
    child_f = f.namespace.get(child_word, None)
    pid = os.fork()
    f.stack.push(pid)
    if pid == 0:
        print("child:", pid)
        child_f(f, 0)
    else:
        print("parent:", pid)
        parent_f(f, 0)
    return i+1

def w_execvp(f, i):
    args = f.stack.pop()
    path = args[0]
    print(f"path {path} args: {args}")
    os.execvp(path, args)
    return i+1

def w_waitpid(f, i):
    pid = f.stack.pop()
    result = os.waitpid(pid, 0)
    f.stack.push(result)
    return i+1

def w_exit(f, i):
    n = f.stack.pop()
    sys.exit(n)
    return i+1

def w_exit_bang(f, i):
    n = f.stack.pop()
    os._exit(n)
    return i+1

