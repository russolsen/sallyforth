import io

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
        state = 'start'
        token = ''
        while True:
            ch = self.read_f()
            #print(f'ch: {ch} typech {type(ch)} state {state}')
            if ch in ['', None]:
                if state in ['word', 'sqstring', 'dqstring']:
                    return [state, token]
                return ['eof', '']
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
                return [state, token]
            elif state == 'start' and ch == "'":
                state = 'sqstring'
            elif state == 'start':
                state = 'word'
                token += ch
            elif state in ['word', 'sqstring'] and \
                 self.whitespace(ch):
                return state, token
            elif state in ['word', 'dqstring', 'sqstring']:
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
    
    kind, token = ts.get_token()
    while kind != 'eof':
        print(kind, token)
        kind, token = ts.get_token()
