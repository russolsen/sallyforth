from lex import forth_prompt
from stack import Stack

class Compiler:
    def __init__(self, name=None):
        self.name = name
        self.instructions = []
        self.offsets = Stack()

    def add_instruction(self, ins):
        self.instructions.append(ins)

    def offset(self):
        return len(self.instructions)

    def push_offset(self):
        self.offsets.push(self.offset())

    def pop_offset(self):
        return self.offsets.pop()

    def _str__(self):
        result = f'Compiler {name} {immediate} '
        for i in self.instructions:
            result += str(i)
            result += ' '
        return result

