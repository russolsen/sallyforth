import io

def to_number(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return None

class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def isstring(self):
        return self.kind == 'string'

    def isword(self):
        return self.kind == 'word'

    def iskeyword(self):
        return self.kind == 'keyword'

    def isnumber(self):
        return self.kind == 'number'

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Token[{self.kind} => {self.value}]'


class PromptInputStream:
    def __init__(self, prompt_f):
        self.prompt_f = prompt_f
        self.buffer = []

    def getc(self):
        try:
            if len(self.buffer) == 0:
                prompt = self.prompt_f()
                line = input(prompt)
                line += '\n'
                self.buffer = list(line)
                self.buffer.reverse()
            return self.buffer.pop()
        except EOFError:
            return ''

class TokenStream:
    def __init__(self, read_f):
        self.read_f = read_f

    def whitespace(self, ch):
        return ch in [' ', '\t', '\n']

    def get_token(self):
        t = self.x_get_token()
        #print("GET token:", t)
        return t

    def x_get_token(self):
        state = 'start'
        token = ''
        while True:
            ch = self.read_f()
            #print(f'ch: {ch} typech {type(ch)} state {state}')
            if ch in ['', None]:
                if state in ['sqstring', 'dqstring']:
                    return Token('string', token)
                if state in ['word']:
                    return Token('word', token)
                return None
            elif state == 'start' and ch == ':':
                token = ch
                state = 'keyword'
            elif state == 'start' and ch in "+-0123456789":
                token = ch
                state = 'number'
            elif state == 'start' and ch == '\\':
                state = 'lcomment'
            elif state == 'lcomment' and ch == '\n':
                state = 'start'
            elif state == 'start' and ch == '(':
                state = 'icomment'
            elif state == 'icomment' and ch == ')':
                state = 'start'
            elif state == 'start' and self.whitespace(ch):
                continue
            elif state == 'start' and ch == '"':
                state = 'dqstring'
            elif state == 'dqstring' and ch == '"':
                return Token('string', token)
            elif state == 'start' and ch == "'":
                state = 'sqstring'
            elif state == 'start':
                state = 'word'
                token += ch
            elif state  == 'number' and self.whitespace(ch):
                n = to_number(token)
                if n:
                    return Token('number', n)
                else:
                    return Token('word', token)
            elif state  == 'word' and self.whitespace(ch):
                return Token('word', token)
            elif state  == 'sqstring' and self.whitespace(ch):
                return Token('string', token)
            elif state == 'keyword' and self.whitespace(ch):
                state = 'start'
                if len(token) == 1:
                    return Token('word', token)
                return Token('keyword', token)
            elif state in ['word', 'dqstring', 'sqstring', 'number', 'keyword']:
                token += ch

def file_token_stream(f):
    return TokenStream(lambda : f.read(1))

def string_token_stream(s):
    sio = io.StringIO(s)
    return file_token_stream(sio)

def prompt_token_stream(prompt_f):
    pis = PromptInputStream(prompt_f)
    return TokenStream(pis.getc)

if __name__ == "__main__":
    x = 0
    
    def pmt():
        global x
        x += 1
        return f'Yes{x}>> '
    
    pis = PromptInputStream(pmt)
    ts = TokenStream(pis.getc)
    
    result = ts.get_token()
    while result:
        print("result:", result)
        result = ts.get_token()
