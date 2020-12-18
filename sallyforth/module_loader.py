import imp
import importlib
#import ast
import copy
from pprint import pprint
from util import word
#from ast_utils import dump

def find_module(name):
    minfo = imp.find_module(name)[0]
    return minfo.name


def build_composite_function(function_asts, name='generated_function'):
    print("*** name:", name)
    #dump(function_asts)
    new_body = []
    for other_f in function_asts:
        print("Other f:", type(other_f))
        #dump(other_f.body)
        new_body.extend(other_f.body)
    new_f = copy.deepcopy(function_asts[0])
    new_f.forth_primitive = False
    new_f.forth_immediate = False
    new_f.name = name
    new_f.body = new_body
    return new_f

def concat_functions(function_asts, name='generated_function'):
    """
    Given an array of function AST objects,
    attempt to produce a new function whose
    body is the concatenation of the existing functions.
    Note that the new function will take the same number
    of arguments as the first function on the list.
    Returns None if it's unable to build the new function.
    """
    new_f = build_composite_function(function_asts, name)
    new_m = ast.Module([new_f])
    print("===== ", name, "====")
    #dump(new_m)
    code = compile(new_m, "*generated*", "exec")
    eval(code)
    f = locals()[name]
    f.ast = new_m.body[0]
    f.forth_primitive = True
    f.forth_immediate = False
    f.forth_inline = False
    print("generated function:", f)
    return f

#m = load_module('m1')
#
#a = m.do1.ast
#b = m.do2.ast
#c = m.do3.ast
#
#f = concat_functions([a,b,c])
#print(f(9))
#
#
