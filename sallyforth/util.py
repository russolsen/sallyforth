def get_attribute(x, name):
    return getattr(x, name, None)

class word:
    def __init__(self, name=None, immediate=False, doc=None):
        self.name = name
        self.immediate = immediate
        self.doc = doc

    def __call__(self, f):
        f.forth_word = True
        if self.name:
            f.forth_name = self.name
        else:
            f.forth_name = f.__name__
        if self.doc:
            f.__doc__ = self.doc
        f.immediate = self.immediate
        return f

def wrap_native_f(f, n, hasreturn):
    if n > 0 and hasreturn:
        def wrapper(forth):
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
    f.operation_type = 'wrapped_primitive'
    f.immediate = False
    return f
   

