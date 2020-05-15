def get_attribute(x, name):
    return getattr(x, name, None)

class word:
    def __init__(self, name=None, immediate=False):
        self.name = name
        self.immediate = immediate

    def __call__(self, f):
        f.forth_word = True
        if self.name:
            f.forth_name = self.name
        else:
            f.forth_name = f.__name__
        f.forth_primitive = True
        f.forth_inline = False
        f.forth_immediate = self.immediate
        return f

def wrap_native_f(f, n, hasreturn):
    if n > 0 and hasreturn:
        def wrapper(forth):
            print("both")
            args = []
            for i in range(n):
                args.append(forth.stack.pop())
            result = f(*args)
            forth.stack.push(result)
    elif n > 0:
        def wrapper(forth):
            args = []
            for i in range(n):
                args.append(forth.stack.pop())
            f(*args)
    elif hasreturn:
        def wrapper(forth):
            forth.stack.push(f(*args))
    else:
        def wrapper(forth):
            print("nothing")
            f()
    return wrapper

def determine_nargs(f, n):
    if n != None:
        return n
    a = inspect.getargs(f.__code__)
    return len(a.args)

def native_word(f, name=None, nargs=None, hasreturn=False):
    nargs = determine_nargs(f, nargs)
    f = wrap_native_f(f, nargs, hasreturn)
    f.forth_type = 'wrapped_primitive'
    f.forth_inline = False
    f.forth_immediate = False
    return f
   

