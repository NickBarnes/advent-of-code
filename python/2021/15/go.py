import re
import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

map = [[int(r) for r in l.strip()] for l in open(input,'r').readlines()]

# rows = len(map)
# cols = len(map[0])
# 
# def neighbours(r,c):
#     v = [(r+1,c)] if r == 0 else [(r-1,c)] if r == rows-1 else [(r-1,c),(r+1,c)]
#     h = [(r,c+1)] if c == 0 else [(r,c-1)] if c == cols-1 else [(r,c-1),(r,c+1)]
#     return v + h

# quick hack algorithm. Could almost certainly be faster if we ordered
# the grey set (the processing queue) by the shortest path in it.

def best(map):
    rows = len(map)
    cols = len(map[0])

    # Give me something to look at while my slow algorithm grinds
    improved = 0
    
    # It's pretty slow to build all these lists
    def neighbours(r,c):
        v = [(r+1,c)] if r == 0 else [(r-1,c)] if r == rows-1 else [(r-1,c),(r+1,c)]
        h = [(r,c+1)] if c == 0 else [(r,c-1)] if c == cols-1 else [(r,c-1),(r,c+1)]
        return v + h

    # corner cell has total risk zero
    final = (rows-1,cols-1)
    shortest = {final:0}
    grey = set([final])

    while grey:
        cell = grey.pop()
        r,c = cell
        d = shortest[cell]
        risk = map[r][c]
        t = d + risk
        for c in neighbours(*cell):
            if c not in shortest or shortest[c] > t:
                grey.add(c) # so we reconsider from there
                shortest[c] = t

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
