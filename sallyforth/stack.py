from collections.abc import Sequence

class Stack(Sequence):
    def __init__(self):
        self.contents = []

    def push(self, x):
        self.contents.append(x)
        return x

    def pop(self):
        return self.contents.pop()

    def __getitem__(self, i):
        return self.contents[i]

    def __len__(self):
        return len(self.contents[i])

    def depth(self):
        return len(self.contents)

    def empty(self):
        return len(self.contents) == 0

    def peek(self):
        return self.contents[-1]

    def reset(self):
        self.contents = []

    def __str__(self):
        result = ''
        for x in self.contents:
            result += str(x)
            result += ' '
        return result
