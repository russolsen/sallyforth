class Stack:
    def __init__(self):
        self.top = -1
        self.stack = 100 * [None]

    def push(self, x):
        #print("stack push", x)
        self.top += 1
        self.stack[self.top] = x
        return x

    def pop(self):
        result = self.stack[self.top]
        #print("stack pop", result)
        self.top -= 1
        if self.top < -1:
            print("stack overpop")
            self.top = -1;
            raise ValueError("Stack underflow")
        return result

    def __iter__(self):
        for i in range(0, self.top+1):
            yield self.stack[i]

    def empty(self):
        return self.top == -1

    def peek(self):
        return self.stack[self.top]

    def reset(self):
        self.top = -1

    def __str__(self):
        result = ''
        for i in range(self.top + 1):
            result += str(self.stack[i])
            result += ' '
        return result
