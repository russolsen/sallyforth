import os
import sys
import atexit
from kernel import Forth
from lex import tokenize
import readline

HistoryFile=".sallyforth"

hist_file = os.path.join(os.path.expanduser("~"), HistoryFile)

class Completer:
    def __init__(self, f):
        self.f = f
    def complete(self, prefix, index):
        self.matching_words = [w for w in self.f.dictionary.keys() if w.startswith(prefix) ]
        try:
            return self.matching_words[index]
        except IndexError:
            return None

def setup_readline(history_path, f):
    completer = Completer(f)
    try:
        readline.read_history_file(history_path)
    except FileNotFoundError:
        pass
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer.complete)
    def save_history():
        readline.write_history_file(history_path)
    atexit.register(save_history)

def setup_forth():
    f = Forth()
    f.defvar("argv", sys.argv[1::])

    source_dir = os.path.dirname(os.path.abspath(__file__))
    startup_file = f'{source_dir}/startup.sf'

    if os.path.exists(startup_file):
        f.execute_file(startup_file)

    return f

def repl(f):
    while True:
        p = f.evaluate_token('*prompt*')
        try:
            line = input(p)
        except KeyboardInterrupt:
            print("<<interrupt>>")
            line = ''
        except EOFError:
            break
    
        tokens = tokenize(line)
        try:
            f.execute_tokens(tokens)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Error:", exc_type)
            print("Error:", exc_value)
            print("Error:", exc_traceback)
    

if __name__ == "__main__":
    f = setup_forth()
    setup_readline(hist_file, f)
    repl(f)
    print("Bye!")
