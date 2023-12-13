import sys
import os
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))
import walk
import file
import interval
import misc

def bitmap(s):
    return sum(1 << i for i,c in enumerate(s) if c == '#')

def check(rows, n, smudges):
    for k in range(min(n+1, len(rows)-n-1)):
        smudges -= int.bit_count(rows[n+k+1] ^ rows[n-k])
        if smudges < 0:
            return False
    return smudges == 0

def score(rows, smudges):
    cols = [bitmap(s) for s in (''.join(col) for col in zip(*rows))]
    rows = [bitmap(s) for s in rows]
    for j in range(len(rows)-1):
        if check(rows, j, smudges):
            return 100 * (j+1)
    for i in range(len(cols)-1):
        if check(cols, i, smudges):
            return i+1
    return 0

def go(filename):
    print(f"results from {filename}:")
    sections = file.sections(filename)
    print("part 1, total of clean mirrors:",
          sum(score(rows, 0) for rows in sections))
    print("part 2, total of mirrors with a single smudge:",
          sum(score(rows, 1) for rows in sections))

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
