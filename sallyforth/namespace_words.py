from wrappers import noop
from namespace import Namespace
from util import word, native_word
#import python_compiler as pc
import inliner
import importlib
from pprint import pprint

@word(doc='Given a name or a word, return the docstring: name-or-word -- docstr')
def doc(forth):
    f = forth.stack.pop()
    if not callable(f):
        f = forth.ns[f].value
    if hasattr(f, '__doc__'):
        forth.stack.push(f.__doc__)
    else:
        forth.stack.push('')

@word(doc='Compile forth word: name -- ')
def compile(forth):
    name = forth.stack.pop()
    var = forth.ns[name]
    word_f = var.value
    new_f = pc.compile_word_f(word_f, name)
    forth.set(name, new_f)

@word(doc='Expand forth word: name -- ')
def inline(forth):
    name = forth.stack.pop()
    var = forth.ns[name]
    word_f = var.value
    new_f = inliner.compile_word_f(word_f, name)
    forth.set(name, new_f)

@word()
def dynamic(forth):
    name = forth.stack.pop()
    isdyn = forth.stack.pop()
    var = forth.ns[name]
    var.dynamic = isdyn

@word()
def native(forth):
    has_return = forth.stack.pop()
    n = forth.stack.pop()
    native_f = forth.stack.pop()
    name = forth.stack.pop()
    wrapped_f = native_word(native_f, name, n, has_return)
    forth.set(name, wrapped_f)

@word("function")
def function_word(forth):
    name = forth.stack.pop()
    var = forth.ns[name]
    word_f = var.value
    def native_f(*args):
        forth.stack.push(args)
        word_f(forth)
        result = forth.stack.pop()
        return result
    forth.stack.push(native_f)

@word(immediate=True)
def readtoken(forth):
    t = forth.stream.get_token()
    def push_token(xforth):
        xforth.stack.push(t)
    return push_token

@word(doc='Load a new native module: modname --')
def load(forth):
    name = forth.stack.pop()
    m = importlib.import_module(name)
    forth.set_constant(name, m)

@word('import', doc='Import a native module, bind all of the module values: modname --')
def w_import(forth):
    name = forth.stack.pop()
    m = importlib.import_module(name)
    forth.ns.import_native_module(m)

@word(doc='Import a module that defines forth words: modname -- ')
def lexicon(forth):
    name = forth.stack.pop()
    m = __import__(name)
    ns = m.__ns__
    forth.namespaces
    ns.parent = forth.namespaces['core']
    forth.namesapces[name] = ns

@word('source', doc='Read an execute a file full of forth code: path --')
def w_source(forth):
    path = forth.stack.pop()
    forth.eval_file(path)

@word('alias')
def w_alias(forth):
    new_name = forth.stack.pop()
    old_name = forth.stack.pop()
    forth.alias(new_name, old_name)

@word("=!")
def equal_bang(forth):
    name = forth.stack.pop()
    value = forth.stack.pop()
    forth.set_constant(name, value)

@word()
def rawdef(forth):
    name = forth.stack.pop()
    value = forth.stack.pop()
    forth.set(name, value)

@word()
def lookup(forth):
    name = forth.stack.pop()
    forth.stack.push(forth.ns[name])

@word(doc='Forget the word from the stack: wordname --')
def forget(forth):
    name = forth.stack.pop()
    del forth.ns[name]

@word('debug-ns')
def debug_ns(forth):
    print('debug ns')
    print(forth.ns.name)
    pprint(forth.ns.includes)
    pprint(forth.ns.contents)

@word('*ns*')
def star_ns_star(forth):
    forth.stack.push(forth.ns)

@word('new-ns')
def new_ns(forth):
    name = forth.stack.pop()
    core = forth.namespaces['core']
    namespace = Namespace(name, [core])
    forth.namespaces[name] = namespace

@word('include')
def include_ns(forth):
    name = forth.stack.pop()
    included = forth.namespaces[name]
    forth.ns.include_ns(included)

@word('set-ns')
def set_ns_word(forth):
    name = forth.stack.pop()
    forth.set_ns(name)

@word('ns?')
def ns_question(forth):
    name = forth.stack.pop()
    forth.stack.push(name in forth.namespaces)

@word(':', True)
def colon(forth):
    name = forth.stream.get_token().value
    tok = forth.stream.get_token(True)
    docstring = None
    if tok.iscomment():
        docstring = tok.value
        tok = None
    body = forth.compile_next(tok)
    if docstring:
        body.__doc__ = docstring
    forth.set(name, body)
    forth.core.set_constant('*last-word*', name)
    return noop

@word()
def setdoc(forth):
    word = forth.stack.pop()
    doc = forth.stack.pop()
    f = forth.ns[word].value
    f.__doc__ = doc
