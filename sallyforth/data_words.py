from util import word, get_attribute
from unique import Unique

@word('[list]')
def w_bounded_list(f):
    """Create a list from delimted values on the stack.
    [list]
    (marker a b c marker -- [a b c]
    """
    marker = f.stack.pop()
    l = []
    if f.stack.empty():
        raise ValueError("Stack underflow")
    x = f.stack.pop()
    while x != marker:
        l.append(x)
        if f.stack.empty():
            raise ValueError("Stack underflow")
        x = f.stack.pop()
    l.reverse()
    f.stack.push(l)

@word('->list')
def w_list(f):
    n = f.stack.pop()
    l = []
    for i in range(n):
        l.append(f.stack.pop())
    f.stack.push(l)

@word()
def w_map(f):
    word = f.stack.pop()
    l = f.stack.pop()

    word_f = f.lookup(word)
    print(word_f)
    result = []

    for item in l:
        f.stack.push(item)
        word_f(f)
        result.append(f.stack.pop())

    f.stack.push(result)

@word()
def w_reduce(f):
    l = f.stack.pop()
    word = f.stack.pop()
    print(f'L: {l} word {word}')
    word_f = f.lookup(word)

    if len(l) <= 0:
        f.stack.push(None)
    elif len(l) == 1:
        f.stack.push(l[0])
    else:
        result = l[0]
        l = l[1::]
        for item in l:
            f.stack.push(result)
            f.stack.push(item)
            word_f(f)
            result = f.stack.pop()
        f.stack.push(result)

@word('@@')
def w_thread(f):
    contents = f.stack.pop()
    print("Contents:", contents)
    result = contents[0]
    for field in contents[1::]:
        print("Result:", result)
        if isinstance(field, str) and hasattr(result, field):
            result = getattr(result, field)    # result.field
        else:
            result = result[field]             # result[field]
    f.stack.push(result)

@word('list->map')
def w_list_to_map(f):  # list->map
    l = f.stack.pop()
    result = {}
    for i in range(0, len(l), 2):
        result[l[i]] = l[i+1]
    f.stack.push(result)

@word()
def w_get(f):
    name = f.stack.pop()
    m = f.stack.pop()
    result = m[name]
    f.stack.push(result)

@word()
def w_getattribute(f):
    name = f.stack.pop()
    x = f.stack.pop()
    result = x.__getattribute__(name)
    f.stack.push(result)
