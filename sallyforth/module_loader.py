import imp
import importlib
import ast
import copy
from pprint import pprint
from util import word
#from ast_utils import dump

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.index = {}
    def visit_FunctionDef(self, node):
        self.index[node.name] = node

def find_module(name):
    minfo = imp.find_module(name)[0]
    return minfo.name

def parse_module(path):
    with open(path) as f:
        text = f.read()
    tree = ast.parse(text)
    ast.fix_missing_locations(tree)
    return tree

def index_functions(tree):
    fv = FunctionVisitor()
    fv.visit(tree)
    return fv.index

def function_index(module_name):
    path = find_module(module_name)
    tree = parse_module(path)
    return index_functions(tree)

def add_ast(m, function_index):
    names = dir(m)
    for name in names:
        if name in function_index:
            f = getattr(m, name)
            f.ast = function_index[name]
    return m

def load_module(name):
    """
    Loads and returns the module with name.
    The difference is that this function also adds
    the Python ast to each function in the module
    along the way.
    """
    findex = function_index(name)
    m = importlib.import_module(name)
    add_ast(m, findex)
    return m

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
