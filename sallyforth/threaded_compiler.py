from tokenstream import Token
from wrappers import value_f, inner_f
LBrace = Token('word', '{')
RBrace = Token('word', '}')

def compile_word(forth, w):
    name = w.value
    var = forth.ns[name]
    value = var.value
    if value.immediate:
        result = value(forth)
    elif var.dynamic:
        result = var
    else:
        result = value
    return result

def compile_token(forth, t):
    if t.kind in ['number', 'string', 'keyword']:
        f = value_f(t.value)
    elif t.kind == 'word':
        f = compile_word(forth, t)
    else:
        print(f'{n}??')
        raise ValueError()
    return f

def compile_value(contents, v):
    contents.append(v)
    return contents

def compile_block(forth, stream, wrap_block):
    contents = []
    t = stream.get_token()
    while t != RBrace:
        compile_value(contents, compile_next(forth, stream, t))
        t = stream.get_token()
    f = inner_f(contents)
    if wrap_block:
        f = value_f(f)
    return f
 
def compile_next(forth, stream, current_token=None, wrap_block=False):
    if current_token:
        t = current_token
    else:
        t = stream.get_token()

    if t == None:
        return None

    if t != LBrace:
        return compile_token(forth, t)
    
    return compile_block(forth, stream, wrap_block)

def eval_stream(forth, stream):
    t = stream.get_token()
    while t:
        compiled = compile_next(forth, stream, t, True)
        compiled(forth)
        t = stream.get_token()
