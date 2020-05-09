from tokenstream import Token
from wrappers import value_f, inner_f, ref_f

LBrace = Token('word', '{')
RBrace = Token('word', '}')

def compile_word(forth, w):
    name = w.value
    var = forth.ns[name]
    value = var.value

    if value.forth_immediate:
        return value(forth)
    elif var.dynamic:
        return ref_f(var)
    else:
        return value

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
    #print("compiling", v, v.__dict__)
    if v.forth_inline and v.forth_contents:
        contents.extend(v.forth_contents)
    else:
        contents.append(v)
    return contents

def compile_next(forth, stream, current_token=None):
    if current_token:
        t = current_token
    else:
        t = stream.get_token()

    if t == None:
        return None

    if t != LBrace:
        return compile_token(forth, t)

    contents = []
    t = stream.get_token()
    while t != RBrace:
        compile_value(contents, compile_next(forth, stream, t))
        t = stream.get_token()
    f = inner_f(contents)
    return f

def eval_stream(forth, stream):
    t = stream.get_token()
    while t:
        compiled = compile_next(forth, stream, t)
        #print(f"*** compiled {t} => {compiled}")
        compiled(forth)
        t = stream.get_token()
