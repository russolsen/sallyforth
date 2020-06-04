import os
import sys
import atexit
import readline
import traceback
import argparse
from kernel import Forth
from tokenstream import prompt_token_stream

HistoryFile='.sallyforth'

hist_file = os.path.join(os.path.expanduser('~'), HistoryFile)

class Completer:
    """
    Supply the list of words available in the current namespace.
    """
    def __init__(self, f):
        self.f = f
    def complete(self, prefix, index):
        self.matching_words = \
                [w for w in self.f.ns.all_keys() if w.startswith(prefix)]
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
    readline.parse_and_bind('tab: complete')
    readline.set_completer_delims(" \t\n()[{]}\\|;:\"',")
    readline.set_completer(completer.complete)
    def save_history():
        readline.write_history_file(history_path)
    atexit.register(save_history)

def setup_forth(run_startups, additional_scripts):
    f = Forth()
    for s in additional_scripts:
        f.eval_file(s)
    f.eval_string(": *i-cmd* { 'Icmd: p p }")

    return f

def repl(f):
    print('Sally welcomes you!')
    while True:
        try:
            prompt = f.eval_string_r('*prompt*')
            try:
                line = input(prompt)
            except EOFError:
                return
            try:
                if len(line) > 0 and line[0] == '/':
                    print('special handline:', line)
                    f.stack.push(line)
                    f.eval_string('*i-cmd*')
                else:
                    f.eval_string(line)
            except:
               traceback.print_exc()
        except KeyboardInterrupt:
            print()

def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nostartup', help='Skip startup scripts', action='store_true')
    parser.add_argument('scripts', nargs='*')
    args = parser.parse_args()
    return (not args.nostartup), args.scripts

if __name__ == '__main__':
    run_startup, scripts = process_args()
    f = setup_forth(run_startup, scripts)
    setup_readline(hist_file, f)
    repl(f)
    print('Bye!')
