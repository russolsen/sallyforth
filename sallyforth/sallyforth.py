import os
import sys
import atexit
import readline
import traceback
from kernel import Forth
from tokenstream import prompt_token_stream

HistoryFile=".sallyforth"

hist_file = os.path.join(os.path.expanduser("~"), HistoryFile)

class Completer:
    def __init__(self, f):
        self.f = f
    def complete(self, prefix, index):
        self.matching_words = [w for w in self.f.namespace.all_keys() if w.startswith(prefix) ]
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
    def prompt_f():
        return f.evaluate_string('*prompt*')
    return prompt_token_stream(prompt_f)    

def setup_forth():
    source_dir = os.path.dirname(os.path.abspath(__file__))
    startup_file = f'{source_dir}/startup.sf'

    if os.path.exists(startup_file):
        f = Forth(startup_file)
    else:
        f = Forth()
    return f

def repl(stream, f):
    f.execute_token_stream(stream)

if __name__ == "__main__":
    f = setup_forth()
    stream = setup_readline(hist_file, f)
    repl(stream, f)
    print("Bye!")
