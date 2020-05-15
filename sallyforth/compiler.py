from tokenstream import Token
from wrappers import value_f, inner_f, inner2_f, inner3_f, ref_f, noop
from recoder import concat_functions

LBrace = Token('word', '{')
RBrace = Token('word', '}')

def composite_function(contents):
    asts = []
    for f in contents:
        ast = getattr(f, 'ast', None)
        if not ast:
            print("No ast for:", f)
            return None
        asts.append(ast)
    return concat_functions(asts)

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
    print("compiling", v, v.__dict__)
    if v.forth_inline and v.forth_contents:
        contents.extend(v.forth_contents)
    else:
        contents.append(v)
    return contents

def compile_block(forth, stream, wrap_block):
    contents = []
    t = stream.get_token()
    while t != RBrace:
        compile_value(contents, compile_next(forth, stream, t))
        t = stream.get_token()

    if len(contents) == 0:
        f = noop
    elif len(contents) == 1:
        f = contents[0]
    elif len(contents) == 2:
        f = inner2_f(contents[0], contents[1])
    elif len(contents) == 3:
        f = inner3_f(contents[0], contents[1], contents[2])
    else:
        f = inner_f(contents)

    if wrap_block:
        f = value_f(f)
    return f
 
def xxx_compile_block(forth, stream, wrap_block):
    contents = []
    t = stream.get_token()
    while t != RBrace:
        compile_value(contents, compile_next(forth, stream, t))
        t = stream.get_token()

    f = composite_function(contents)
    if not f:
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
        #print(f"*** compiled {t} => {compiled}")
        compiled(forth)
        t = stream.get_token()
