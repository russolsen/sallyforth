class Reference:
    def __init__(self, var):
        self.var = var

    def __call__(self, forth):
        #print("indirect call on", self.var.name)
        return self.var.value(forth)

    @property
    def forth_immediate(self):
        return self.var.value.forth_immediate

    @property
    def forth_contents(self):
        return self.var.value.forth_contents

    @property
    def forth_primitive(self):
        return self.var.value.forth_primitive

    @property
    def forth_name(self):
        return self.var.value.forth_name

    @property
    def forth_inline(self):
        return self.var.value.forth_inline

def ref_f(var):
    return Reference(var)
        
def value_f(value):
    def push_constant(f):
        f.stack.push(value)
    push_constant.forth_inline = False
    push_constant.forth_primitive = True
    push_constant.forth_name = 'pushv'
    push_constant.forth_immediate = False
    return push_constant

def inner_f(contents):
    def inner(forth):
        for fn in contents:
            fn(forth)
    inner.forth_primitive = False
    inner.forth_immediate = False
    inner.forth_contents = contents
    inner.forth_inline = False
    return inner

def noop(value):
    pass
