import re
import sys
import walk

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

map = [[int(r) for r in l.strip()] for l in open(input,'r').readlines()]

def best(map):
    walker = walk.Walk(lambda _,__: True, lambda pos: map[pos[0]][pos[1]])
    risks = walker.walk(map, (len(map)-1,len(map[0])-1))
    return risks[(0,0)]

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
