from pluralizer import Pluralizer
from contextlib import redirect_stdout
pluarizer = Pluralizer()

with open('words.txt', 'r') as f:
    lines = f.readlines()

new_lines = set()
for line in lines:
    word = line.strip()
    new_lines.add(word)
    if pluarizer.isSingular(word):
        new_lines.add(pluarizer.plural(word))


with open('words3.txt', 'w') as f:
    with redirect_stdout(f):
        for line in sorted(new_lines):
            print(line)