class Stack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        self.stack.append(x)
        return x

    def pop(self):
        return self.stack.pop()

    def __iter__(self):
        for x in self.stack:
            yield x

    def depth(self):
        return len(self.stack)

    def empty(self):
        return len(self.stack) == 0

    def peek(self):
        return self.stack[-1]

    def reset(self):
        self.stack = []

    def __str__(self):
        result = ''
        for x in self.stack:
            result += str(x)
            result += ' '
        return result
