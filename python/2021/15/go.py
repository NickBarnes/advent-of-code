import re
import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

map = [[int(r) for r in l.strip()] for l in open(input,'r').readlines()]

# replaced a set with a priority queue and my (still stupid hack)
# algorithm went from 45 seconds to 1.5.

from queue import PriorityQueue

def best(map):
    rows = len(map)
    cols = len(map[0])
    mapmap = {(r,c) : map[r][c] for r in range(rows) for c in range(cols)}

    # Give me something to look at while my slow algorithm grinds
    improved = 0
    
    def neighbours(r,c):
        if r > 0:
            yield (r-1,c)
        if r < rows-1:
            yield (r+1,c)
        if c > 0:
            yield (r, c-1)
        if c < cols-1:
            yield (r, c+1)

    # corner cell has total risk zero
    final = (rows-1,cols-1)
    shortest = {final:0}
    grey = PriorityQueue()
    grey.put((0, final))

    while not grey.empty():
        total, cell = grey.get()
        row,col = cell
        if shortest[cell] != total: # already processed at a lower length
            continue
        risk = mapmap[cell]
        total += risk
        for c in neighbours(row,col):
            if c not in shortest or shortest[c] > total:
                grey.put_nowait((total, c)) # so we reconsider from there
                shortest[c] = total

                # chatter
                improved += 1
                if improved % 1000000 == 0:
                    print(f"improved {improved} cells")
    print(f"improved {improved} cells")

    return shortest[0,0]

smallbest = best(map)
print(f"lowest total risk of a path top-left to bottom-right (answer one): {smallbest}")

# add two cells together, wrapping from 9 to 1
def add(x,n): return (((x-1)+n) % 9)+1

# make a map five times wider, each duplicate bumped by one
def wide(map):
    return [[c for l in ([add(c,i) for c in r] for i in range(5)) for c in l] for r in map]
# make a map five times taller, each duplicate bumped by one
def tall(map):
    return [r for m in ([[add(c,i) for c in r] for r in map] for i in range(5)) for r in m]

# the big map
bigmap=tall(wide(map))
bigbest = best(bigmap)

print(f"lowest total risk of a path top-left to bottom-right in enlarged map (answer two): {bigbest}")
