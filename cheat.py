WORDS_FILE = "words3.txt"

import pyautogui
from tqdm import tqdm
import time

print('TO USE PLEASE SET TOP LEFT AND MUL ON LINES 74-75, CHANGE GRID.TXT, AND DELETE THE EXIT() on LINE 8')
exit()

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

with open(WORDS_FILE, 'r') as f:
    n = len(f.readlines())

paths = {}

with open(WORDS_FILE, 'r') as f:
    for line in tqdm(f, desc='trying words', total=n):
        path = valid_word(line.strip())
        if path:
            paths[line.strip()] = path

TOPLEFT = (1040, 420) # x and y coordinate of grid[0][0] on the screen
MUL = 60 # how much distance between each grid element on the screen

def get_screen_c(x):
    return TOPLEFT[0] + MUL*x
def get_screen_r(y):
    return TOPLEFT[1] + MUL*y
def moveTo(r, c, delay=0.0):
    pyautogui.dragTo(get_screen_c(c), get_screen_r(r), button='left', mouseDownUp=False, duration=delay)

print('STARTING IN 5')
time.sleep(5)

MIN_DELAY = 0 # change if you want it slower

for word, path in sorted(paths.items(), key=lambda x: len(x[0]), reverse=True):
    rstart, cstart = path[0]
    moveTo(rstart, cstart, delay=MIN_DELAY)
    pyautogui.mouseDown()
    for r, c in path[1:]:
        moveTo(r, c, delay=MIN_DELAY)
    pyautogui.mouseUp()
