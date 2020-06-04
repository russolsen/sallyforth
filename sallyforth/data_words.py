from util import word, get_attribute
from unique import Unique

@word('[list]')
def w_bounded_list(forth):
    """Create a list from delimted values on the stack.
    [list]
    (marker a b c marker -- [a b c])
    """
    marker = forth.stack.pop()
    l = []
    if forth.stack.empty():
        raise ValueError("Stack underflow")
    x = forth.stack.pop()
    while x != marker:
        l.append(x)
        if forth.stack.empty():
            raise ValueError("Stack underflow")
        x = forth.stack.pop()
    l.reverse()
    forth.stack.push(l)

@word('->list')
def w_list(forth):
    n = forth.stack.pop()
    l = []
    for i in range(n):
        l.append(forth.stack.pop())
    forth.stack.push(l)

@word()
def w_map(forth):
    word = forth.stack.pop()
    l = forth.stack.pop()

    word_f = forth.lookup(word)
    print(word_f)
    result = []

    for item in l:
        forth.stack.push(item)
        word_f(forth)
        result.append(forth.stack.pop())

    forth.stack.push(result)

@word()
def w_reduce(forth):
    l = forth.stack.pop()
    word = forth.stack.pop()
    print(f'L: {l} word {word}')
    word_f = forth.lookup(word)

    if len(l) <= 0:
        forth.stack.push(None)
    elif len(l) == 1:
        forth.stack.push(l[0])
    else:
        result = l[0]
        l = l[1::]
        for item in l:
            forth.stack.push(result)
            forth.stack.push(item)
            word_f(forth)
            result = forth.stack.pop()
        forth.stack.push(result)

@word('@@')
def w_thread(forth):
    contents = forth.stack.pop()
    #print("Contents:", contents)
    result = contents[0]
    for field in contents[1::]:
        #print("Result:", result)
        if isinstance(field, str) and hasattr(result, field):
            result = getattr(result, field)    # result.field
        else:
            result = result[field]             # result[field]
    forth.stack.push(result)

@word('list->map')
def w_list_to_map(forth):  # list->map
    l = forth.stack.pop()
    result = {}
    for i in range(0, len(l), 2):
        result[l[i]] = l[i+1]
    forth.stack.push(result)

@word()
def w_get(forth):
    name = forth.stack.pop()
    m = forth.stack.pop()
    result = m[name]
    forth.stack.push(result)

@word()
def w_getattribute(forth):
    name = forth.stack.pop()
    x = forth.stack.pop()
    result = x.__getattribute__(name)
    forth.stack.push(result)
