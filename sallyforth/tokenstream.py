import io
from kword import Keyword

def to_number(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return None

class Token:
    """
    A Token consists of a string, something like "123" or "dup"
    and kind, also a string, something like "number" or "word".
    """
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.kind == other.kind and self.value == other.value

    def __hash__(self):
        return self.kind.__hash__() + self.value.__hash__()

    def isblock(self):
        return self.kind == 'block'

    def isstring(self):
        return self.kind == 'string'

    def isword(self):
        return self.kind == 'word'

    def iskeyword(self):
        return self.kind == 'keyword'

    def isnumber(self):
        return self.kind == 'number'

    def iscomment(self):
        return self.kind == 'comment'

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Token {self.kind} => {self.value}'

def wtoken(value):
    return Token('word', value)

def stoken(value):
    return Token('string', value)

class PromptInputStream:
    "A stream of characters from in input prompt."
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
    """
    A TokenStream reads and returns one token at a time.
    To create a TokenStream instance you supply the constructor
    with a function that returns one character at a time.
    """
    def __init__(self, read_f):
        self.read_f = read_f
        self.pushed_char = None

    def special(self, ch):
        return ch in ['(', ')', '{', '}']

    def whitespace(self, ch):
        return ch in [' ', '\t', '\n']

    def ender(self, ch):
        return self.whitespace(ch) or self.special(ch)

    def get_token(self, return_comment=False):
        #print("ret comment:", return_comment)
        if return_comment:
            return self.do_get_token()

        t = self.do_get_token()
        while t and t.iscomment():
            t = self.do_get_token()

        return t

    def next_ch(self):
        if self.pushed_char:
            ch = self.pushed_char
            self.pushed_char = None
            return ch
        return self.read_f()

    def unread(self, ch):
        self.pushed_char = ch

    def number_or_word(self, s):
        n = to_number(s)
        if n != None:
            return Token('number', n)
        else:
            return Token('word', s)
 
    def do_get_token(self):
        state = 'start'
        token = ''
        while True:
            ch = self.next_ch()
            if ch in ['', None]:
                if state in ['sqstring', 'dqstring']:
                    return Token('string', token)
                if state in ['word']:
                    return Token('word', token)
                if state == 'comment':
                    return Token('comment', token)
                if state == 'keyword':
                    return Token('keyword', Keyword(token))
                if state == 'number':
                    return self.number_or_word(token)
                return None
            elif state == 'start' and self.special(ch):
                return Token('word', ch)
            elif state == 'start' and ch == ':':
                token = ch
                state = 'keyword'
            elif state == 'start' and ch in "+-0123456789":
                token = ch
                state = 'number'
            elif state == 'start' and ch == '/':
                token = ''
                state = 'comment'
            elif state == 'comment' and ch in ['\n', '/']:
                return Token('comment', token) 
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
            elif state  == 'number' and self.ender(ch):
                self.unread(ch)
                return self.number_or_word(token)
            elif state  == 'word' and self.ender(ch):
                self.unread(ch)
                return Token('word', token)
            elif state  == 'sqstring' and self.whitespace(ch):
                self.unread(ch)
                return Token('string', token)
            elif state == 'keyword' and self.ender(ch):
                self.unread(ch)
                if token in [':']:
                    return Token('word', token)
                return Token('keyword', Keyword(token))
            elif state in ['word', 'dqstring', 'sqstring', 'number', 'keyword', 'comment']:
                token += ch

class MacroTokenStream:
    """
    MacroTokenStream adds a bit of preprocessing to a regular
    token stream. Specifically it turns tokens of the form #aa.bb.cc
    into a sequence of tokens of the form <. aa 'bb 'cc .>.
    """
    def __init__(self, stream):
        self.stream = stream
        self.tokens = []

    def get_more_tokens(self, return_comment):
        raw_token = self.stream.get_token(return_comment)
        if raw_token \
           and raw_token.isword() \
           and raw_token.value[0] == '#':
            parts = raw_token.value[1::].split('.')
            result = [wtoken('<.'), wtoken(parts[0])]
            for p in parts[1::]:
                result.append(stoken(p))
            result.append(wtoken('.>'))
            result.reverse()
            self.tokens.extend(result)
        else:
            self.tokens.append(raw_token)

    def get_token(self, return_comment=False):
        if len(self.tokens) == 0:
            self.get_more_tokens(return_comment)
        if len(self.tokens):
            return self.tokens.pop()
        return None

def file_token_stream(f):
    return MacroTokenStream(TokenStream(lambda : f.read(1)))

def string_token_stream(s):
    sio = io.StringIO(s)
    return file_token_stream(sio)

def prompt_token_stream(prompt_f):
    pis = PromptInputStream(prompt_f)
    return MacroTokenStream(TokenStream(pis.getc))

if __name__ == "__main__":
    x = 0
    def pmt():
        global x
        x += 1
        return f'Yes{x}>> '
    
    pis = PromptInputStream(pmt)
    ts = TokenStream(pis.getc)
    
    result = ts.get_token(True)
    #print("result", result)
    while result:
        print("result:", result)
        result = ts.get_token(True)
