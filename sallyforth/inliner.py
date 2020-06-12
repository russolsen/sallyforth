from wrappers import inner_f

def compile_f(contents, attributes, doc, name):
    new_contents = []
    for f in contents:
        sub_contents = getattr(f, "contents", None)
        if sub_contents:
            new_contents.extend(sub_contents)
        else:
            new_contents.append(f)
    new_func = inner_f(new_contents)
    if attributes:
        new_func.__dict__ = attributes.copy()
    new_func.__doc__ = doc
    new_func.name = name
    return new_func

def compile_word_f(f, name=None):
    contents = getattr(f, 'contents', None)
    if contents and len(contents) > 1:
        return compile_f(contents, f.__dict__, f.__doc__, name)
    return f
