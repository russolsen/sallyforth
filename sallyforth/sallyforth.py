import os
import sys
from kernel import Forth
from lex import tokenize
import readline

HistoryFile=".sallyforth"

histfile = os.path.join(os.path.expanduser("~"), HistoryFile)

try:
    readline.read_history_file(histfile)
except FileNotFoundError:
    pass

source_dir = os.path.dirname(os.path.abspath(__file__))
startup_file = f'{source_dir}/startup.sf'

f = Forth()

class Completer:
    def __init__(self, f):
        self.f = f
    def complete(self, prefix, index):
        self.matching_words = [w for w in self.f.dictionary.keys() if w.startswith(prefix) ]
        try:
            return self.matching_words[index]
        except IndexError:
            return None

completer = Completer(f)

readline.parse_and_bind("tab: complete")
readline.set_completer(completer.complete)

f.defvar("argv", sys.argv[1::])

if os.path.exists(startup_file):
    f.execute_file(startup_file)

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

readline.write_history_file(histfile)

print("Bye!")
