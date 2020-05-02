class Entry:
    def __init__(self, name, value, immed):
        self.name = name
        self.value = value
        self.immediate = immed
        self.inline = False
        self.definition = None

    def get_ivalue(self):
        return self.value

    def get_cvalue(self):
        return self.value

    def __str__(self):
        result = f'Entry {self.name} {self.immediate} {self.inline}\n'
        for x in self.definition:
            result += f'{x}\n'
        return result

class Namespace:
    def __init__(self, name, initial_contents={}, refers=[]):
        self.name = name
        self.contents = initial_contents.copy()
        self.refers = refers.copy()

    def alias(self, new_name, existing_name):
        self.contents[new_name] = self.contents[existing_name]

    def refer(self, ns):
        """
        Add the supplied namespace to the refers list.
        """
        self.refers.append(ns)

    def import_from_module(self, m):
        """
        Import all of the word defining functions in
        module m whose function names start with prefix
        into this namespace. Removes the prefix.
        """
        names = dir(m)
        for name in names:
            if name.startswith("w_"):
                word_name = name[2::]
                #print(f'Setting {word_name} to false')
                self.set(word_name, getattr(m, name))
            elif name.startswith("i_"):
                word_name = name[2::]
                #print(f'Setting {word_name} to true')
                self.set(word_name, getattr(m, name), immediate=True)

    def set(self, name, value, cvalue=None, immediate=False):
        if name not in self.contents:
            entry = Entry(name, value, immediate)
        else:
            entry = self[name]
            entry.value = value
            entry.cvalue = cvalue
            entry.immediate = immediate
        self.contents[name] = entry
        return entry

    def keys(self):
        return self.contents.keys()

    def all_keys(self):
        result = set(self.contents.keys())
        for r in self.refers:
            result = result.union(set(r.contents.keys()))
        return result

    def get(self, key, default):
        if not self.__contains__(key):
            return default
        return self[key]
        
    def __contains__(self, key):
        #print(f'Namespace contains {key}')
        if self.contents.__contains__(key):
            #print(self.contents[key])
            return True
        for r in self.refers:
            if r.__contains__(key):
                return True
        return False

    def local_contains(self, key):
        return self.contents.__contains__(key)

    def __delattr__(self, key):
        return self.contents.__delattr__(key)

    def __setitem__(self, key, x):
        self.contents[key] = x

    def __iter__(self):
        return self.contents.__iter__()

    def __getitem__(self, key):
        #print("get item", key, self.name)
        if key in self.contents:
            return self.contents[key]
        # print("not in local ns")
        for imp in self.refers:
            # print("trying ", imp)
            if key in imp:
                return imp[key]
        # print("not found")
        raise KeyError(key)

    def __str__(self):
        return f'Namespace({self.name})'

if __name__ == '__main__':
    print("main program")
    x = Namespace('x', {'a': 1, 'b': 2})
    print(x['a'])
    y = Namespace('y', {'c': 3, 'd': 4})
    print(y['c'])
    y.refer(x)
    print(y['a'])
