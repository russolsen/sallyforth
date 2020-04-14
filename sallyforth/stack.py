class Stack:
    def __init__(self):
        self.top = -1
        self.stack = 100 * [None]

    def push(self, x):
        # print("stack push", x)
        self.top += 1
        self.stack[self.top] = x
        return x

    def pop(self):
        result = self.stack[self.top]
        # print("stack pop", result)
        self.top -= 1
        if self.top < -1:
            print("stack overpop")
            self.top = -1;
        return result

    def peek(self):
        return self.stack[self.top]

    def __str__(self):
        result = ''
        for i in range(self.top + 1):
            result += str(self.stack[i])
            result += ' '
        return result
