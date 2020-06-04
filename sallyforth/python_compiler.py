#from ast import Attribute, Name, Call, dump, Load, fix_missing_locations, Module, parse, Expr, Expression, FunctionDef, arguments, arg, Interactive, Str
from ast import *
from pprint import pprint
import ast_utils

def fdef_ast(name, body):
    return FunctionDef(name=name, 
            args=arguments(args=[arg(arg='forth', annotation=None)], 
                vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), 
            body=body, decorator_list=[], returns=None)

def call_ast(fname):
    r = Expr(
            value=Call(
                func=Name(id=fname, ctx=Load()),
                args=[Name(id='forth', ctx=Load())],
                keywords=[]))
    return r

def print_ast(name):
    name = name or "generated function"
    r = Expr(
            value=Call(
                func=Name(id="print", ctx=Load()),
                args=[Str(s=name)],
                keywords=[]))
    return r

def compile_f(contents, name):
    d = locals().copy()
    exprs = []
    for i, val in enumerate(contents):
        fname = f'f_{i}'
        d[fname] = val
        exprs.append(call_ast(fname))
    f_ast = fdef_ast('generated_function', exprs)
    m = Module(body=[f_ast])
    fix_missing_locations(m)
    code = compile(m, 'source', 'exec')
    exec(code, d)
    f = d['generated_function']
    f.immediate = False
    f.operation_type = 'compiled'
    f.name = name
    f.contents = contents
    return f

def compile_word_f(f, name=None):
    """
    Given a Forth word function return an equivalent function.
    Compile_word_f works by building up a Python AST for a function
    that executes all of the content functions and then compiling
    it.

    The idea is that compiled functions skip all of the overhead
    of running thru the contents array at runtime.
    """
    contents = getattr(f, 'contents', None)
    if contents and len(contents) > 1:
        return compile_f(contents, name)
    return f
