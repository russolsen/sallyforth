from wrappers import inner_f

def compile_f(contents, name):
    new_contents = []
    for f in contents:
        sub_contents = getattr(f, "contents", None)
        if sub_contents:
            new_contents.extend(sub_contents)
        else:
            new_contents.append(f)
    new_func = inner_f(new_contents)
    new_func.name = name
    return new_func

def compile_word_f(f, name=None):
    contents = getattr(f, 'contents', None)
    if contents and len(contents) > 1:
        return compile_f(contents, name)
    return f
