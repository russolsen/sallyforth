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
        f.forth_type = 'primitive'
        f.forth_inline = False
        f.forth_immediate = self.immediate
        return f

