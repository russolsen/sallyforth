from collections import UserString

class Keyword(UserString):
    def __init__(self, value):
        value = value[1::]
        UserString.__init__(self, value)

    def __call__(self, d):
        return d[self]

    def __repr__(self):
        return ':' + str(self)
