THEME = "Just the essentials"

import pyautogui
from tqdm import tqdm
import time
from llm import generate
import pickle
import os

grid = []
letters = []
with open('grid.txt', 'r') as f:
    for line in f:
        grid.append(list(line.strip()))
        letters.extend(list(line.strip()))

starts = {}
adjacency_list = {}

def get_neighbors(rval, cval) -> list[tuple[int, int]]:
    neighbors = []
    for r in range(max(0, rval-1), min(len(grid)-1, rval+1)+1):
        for c in range(max(0, cval-1), min(len(grid[0])-1, cval+1)+1):
            if r != rval or c != cval:
                neighbors.append((r, c, grid[r][c]))
    return neighbors

for r in range(len(grid)):
    for c in range(len(grid[0])):
        val = grid[r][c]
        if val in starts:
            starts[val].append((r, c))
        else:
            starts[val] = [(r, c)]
        adjacency_list[r, c] = get_neighbors(r, c)

def check_valid(r, c, val, word, visited: list):
    if val != word[0]:
        return []
    visited.append((r, c))
    if len(word) == 1: 
        return visited
    for rnew, cnew, valnew in adjacency_list[r, c]:
        if (rnew, cnew) not in visited:
            ret = check_valid(rnew, cnew, valnew, word[1:], visited)
            if ret:
                return ret
    visited.remove((r, c))
    return []

def valid_word(word):
    if len(word) < 4:
        return []
    word = word.upper()
    if word[0] not in starts:
        return []
    for r, c in starts[word[0]]:
        path = check_valid(r, c, grid[r][c], word, [])
        if path:
            return path
    return []

with open('words.txt', 'r') as f:
    n = len(f.readlines())

paths = {}

with open('words3.txt', 'r') as f:
    for line in tqdm(f, desc='trying words', total=n):
        path = valid_word(line.strip())
        if path:
            paths[line.strip()] = path

words = [word for word in paths]

# genmodel
files = os.listdir('themes')
if THEME in files:
    print('loading previous openai response')
    with open(f'themes/{THEME}', 'rb') as f:
        generated = pickle.load(f)
else:
    print('dumping new openai response')
    sys_prompt = f"""
    Given the following theme: {THEME}
    You will be instructed to pick the most likely words that fit with the theme
    Generate the words and only the words with a space separating each word
    """
    user_prompt = f"""
    Pick the most likely words associated with the theme using the following word list:
    {words}
    """
    with open(f'themes/{THEME}', 'wb') as f:
        generated = generate(sys_prompt, user_prompt)
        pickle.dump(generated, f)
    
new_words = generated.choices[0].message.content.split()
to_do = []
for word in new_words:
    if word in paths:
        to_do.append(paths[word])
for key in sorted(paths.keys() - set(new_words)):
    to_do.append(paths[key])

topleft = (630, 570)
mul = 42

def get_screen_c(x):
    return topleft[0] + mul*x
def get_screen_r(y):
    return topleft[1] + mul*y
def moveTo(r, c, delay=0.0):
    pyautogui.moveTo(get_screen_c(c), get_screen_r(r), duration=delay)

print('STARTING IN 5')
time.sleep(5)

MIN_DELAY = 0

for path in to_do:
    for r, c in path:
        moveTo(r, c, delay=MIN_DELAY)
        pyautogui.click()
    pyautogui.click()