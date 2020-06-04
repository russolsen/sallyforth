from ast import *
import ast

forth_stack_ast = Attribute(value=Name(id='forth', ctx=Load()),
                  attr='stack', ctx=Load())

forth_push_ast = Attribute(value=forth_stack_ast, attr='push', ctx=Load())

def push_ast(val_ast):
    return call(func=forth_push_ast, args=[val_ast], keywords=[])

def value_ast(value):
    print("value ast:", value)
    if isinstance(value, str):
        return Str(value)
    elif isinstance(value, int):
        return Num(value)
    elif isinstance(value, float):
        return Num(value)
    else:
        return None
 
def push_value_ast(value, name='constant'):
    vast = value_ast(value)
    if vast:
        result = FunctionDef(
            name=name,
            vararg=None,
            kw_defaults=[],
            decorator_list=[],
            args=arguments(args=[arg(arg='forth', annotation=None)], vararg=None, kwonlyargs=[], kw_defaults=[], defaults=[]),
            body=[Expr(value=push_ast(vast))])
        fix_missing_locations(result)
        return result
    return None



def dump(x):
    #print("dump", x, type(x))
    if x == None:
        print("None!")
    elif isinstance(x,str):
        print("String:", x)
    elif isinstance(x,list) or isinstance(x, tuple):
        for el in x:
            print("List dump:")
            dump(el)
    else:
        ast.dump(x)

def indent(s, level=0):
    spaces = "  " * level
    return spaces + str(s)

def nl(s):
    return s + "\n"

def dump_coll(kind, ast, level):
    n = str(len(ast))
    result = nl(indent(kind + "(" + n + ") =>", level))
    for x in ast:
        result += dump(x, level+1)
    return result

def dump_tuple(ast, level=0):
    return dump_coll("tuple", ast, level)

def dump_list(ast, level=0):
    return dump_coll("list", ast, level)

def dump_plain_str(x, level=0):
    return nl(indent("str:" + x, level))

def dump_expr(x, level=0):
    return nl(indent("expr!!", level))

def dump_name(x, level=0):
    return nl(indent(f'name({x.id})', level))

def ast_dump(x, level=0):
    return nl(indent(ast.dump(x), level))

def dump_expr(x, level=0):
    return nl(indent("Expr:", level)) \
            + dump(x.value, level+1)

def dump_module(m, level=0):
    return nl(indent("Module:", level)) + \
           dump_coll("body", m.body, level+1)

def dump_assign(a, level=0):
    return nl(indent("Assign:", level)) + \
           dump_coll("targets", a.targets, level+1) + \
           dump(a.value, level+1)

def dump_call(c, level=0):
    return nl(indent("Call", level)) + \
           dump(c.func, level+1) + \
           dump_coll("Args:", c.args, level+1)

def dump_fdef(fd, level=0):
    return nl(indent("FunctionDef", level)) + \
           nl(indent(fd.name, level+1)) + \
           dump_coll(str(type(fd.body)), fd.body, level+1)

def dump_attr(a, level=0):
    return nl(indent("Attr", level)) + \
            dump(a.attr, level+1) + \
            dump(a.value, level+1)

switcher = {
       list: dump_list,
       tuple: dump_tuple,
       str: dump_plain_str,
       Name: dump_name,
       Expr: dump_expr,
       FunctionDef: dump_fdef,
       Module: dump_module,
       Assign: dump_assign,
       Attribute: dump_attr,
       Call: dump_call}

def dump(ast, level=0):
    print(">>Dump", ast)
    if ast == None:
        return nl(indent("None", level))
    t = type(ast)
    if t in switcher:
        f = switcher[t]
        return f(ast, level)
    else:
        print("?????", ast)
        return str(ast)


