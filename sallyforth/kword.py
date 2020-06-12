from collections import UserString

class Keyword(UserString):
    """
    A Keyword is more or less a specialized string. The main difference
    between strings and keywords is that Keyswords, when called as a function
    with a dictionary as an argument will look themselves up in the dictionary.
    """
    def __init__(self, value):
        value = value[1::]
        UserString.__init__(self, value)

    def __call__(self, forth):
        d = forth.stack.pop()
        forth.stack.push(d[self])

    def __repr__(self):
        return ':' + str(self)
