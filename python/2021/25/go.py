import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

def go(filename):
    print(f"results from {filename}:")
    chars = [[c for c in r.strip()] for r in open(filename,'r') if r.strip()]
    rows = len(chars)
    cols = len(chars[0])
    
    round = 0
    while True:
        moved = False
        moves = []
        for r in range(rows):
            for c in range(cols):
               if chars[r][c] == '>' and chars[r][(c + 1) % cols] == '.':
                   moves.append((r,c))
        for r,c in moves:
               moved = True
               chars[r][c] = '.'
               chars[r][(c+1) % cols] = '>'
        moves = []
        for r in range(rows):
            for c in range(cols):
               if chars[r][c] == 'v' and chars[(r + 1) % rows][c] == '.':
                   moves.append((r,c))
        for r,c in moves:
               moved = True
               chars[r][c] = '.'
               chars[(r+1) % rows][c] = 'v'
        round += 1
        if not moved:
               print(round)
               break

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
