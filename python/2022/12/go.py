import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

def go(filename):
    print(f"results from {filename}:")
    chars = file.chars(filename)
    grid = [[0 if c == 'S' else 25 if c == 'E' else ord(c)-ord('a') for c in row] for row in chars]
    start = next((i, row.index('S')) for i, row in enumerate(chars) if 'S' in row)
    end = next((i, row.index('E')) for i, row in enumerate(chars) if 'E' in row)

    # reachability going down: may climb any amount but not descend more than 1
    def weight(a,b):
        return 1 if grid[a[0]][a[1]] - grid[b[0]][b[1]] <= 1 else None

    far = walk.walk(len(grid), len(grid[0]), weight, end, diagonal=False)

    print(f"shortest path from start to end is {far[start]}")
    shortest_climb = min(v for p,v in far.items() if grid[p[0]][p[1]] == 0)
    print(f"shortest path from low point to end is {shortest_climb}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
