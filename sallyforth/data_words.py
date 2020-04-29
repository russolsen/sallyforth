from unique import Unique

def w_unique(f, ip):  # pushes a uique object.
    f.stack.push(Unique())
    return ip+1

def w_map(f, ip):
    word = f.stack.pop()
    l = f.stack.pop()

    word_f = f.namespace.get(word, None)
    result = []

    for item in l:
        f.stack.push(item)
        word_f(f, 0)
        result.append(f.stack.pop())

    f.stack.push(result)
    return ip+1

def w_reduce(f, ip):
    l = f.stack.pop()
    word = f.stack.pop()

    word_f = f.namespace.get(word, None)

    if len(l) <= 0:
        f.stack.push(None)
    elif len(l) == 1:
        f.stack.push(l[0])
    else:
        result = l[0]
        l = l[1::-1]
        for item in l:
            f.stack.push(result)
            f.stack.push(item)
            word_f(f, 0)
            result = f.stack.pop()
        f.stack.push(result)

    return ip+1

def w_bounded_list(f, ip):
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
    return ip+1

def w_to_arglist(f, ip):
    l = f.stack.pop()
    f.stack.push(Arglist(l))
    return ip+1

def w_list(f, ip):    # ->list
    n = f.stack.pop()
    l = []
    for i in range(n):
        l.append(f.stack.pop())
    f.stack.push(l)
    return ip+1

def w_thread(f, i):    # @@
    contents = f.stack.pop()
    result = contents[0]
    for field in contents[1::]:
        if isinstance(field, str) and hasattr(result, field):
            result = getattr(result, field)    # result.field
        elif isinstance(field, Arglist):
            result = result(*field)            # result(*field)
        else:
            result = result[field]             # result[field]
    f.stack.push(result)
    return i+1


ListMarker = object()

def w_startlist(f, i):   # [
    f.stack.push(ListMarker)
    return i+1

def w_endlist(f, i):    # ]
    l = []
    x = f.stack.pop()
    while x != ListMarker:
        l.append(x)
        x = f.stack.pop()
    l.reverse()
    f.stack.push(l)
    return i+1

MapMarker = object()

def w_startmap(f, i):   # {
    f.stack.push(MapMarker)
    return i+1

def w_endmap(f, ip):    # }
    l = []
    x = f.stack.pop()
    while x != MapMarker:
        l.append(x)
        x = f.stack.pop()
    if (len(l) % 2) != 0:
        print('Maps need even number of entries.')
        return i+1
    l.reverse()
    result = {}
    for i in range(0, len(l), 2):
        result[l[i]] = l[i+1]
    f.stack.push(result)
    return ip+1

def w_list_to_map(f, ip):  # list->map
    l = f.stack.pop()
    result = {}
    for i in range(0, len(l), 2):
        result[l[i]] = l[i+1]
    f.stack.push(result)
    return ip+1

def w_get(f, i):
    name = f.stack.pop()
    m = f.stack.pop()
    result = m[name]
    f.stack.push(result)
    return i+1

def w_getattribute(f, i):
    name = f.stack.pop()
    x = f.stack.pop()
    result = x.__getattribute__(name)
    f.stack.push(result)
    return i+1

def w_def(f, i):
    value = f.stack.pop()
    name = f.stack.pop()
    f.defvar(name, value)
    # print('name', name, 'value', value)
    return i+1


