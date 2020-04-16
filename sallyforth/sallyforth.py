import os
from kernel import Forth
from lex import tokenize


source_dir = os.path.dirname(os.path.abspath(__file__))
startup_file = f'{source_dir}/startup.sf'
print(startup_file)

f = Forth()

if os.path.exists(startup_file):
    f.execute_file(startup_file)

while True:
    p = f.evaluate_token('*prompt*')
    line = input(p)
    tokens = tokenize(line)
    f.execute_tokens(tokens)
