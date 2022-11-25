import re
import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

map = [[int(r) for r in l.strip()] for l in open(input,'r').readlines()]

rows = len(map)
cols = len(map[0])

def neighbours(r,c):
    v = [(r+1,c)] if r == 0 else [(r-1,c)] if r == rows-1 else [(r-1,c),(r+1,c)]
    h = [(r,c+1)] if c == 0 else [(r,c-1)] if c == cols-1 else [(r,c-1),(r,c+1)]
    return v + h

final = (rows-1,cols-1)
grey = set([final])
shortest = {final:(0,[])}

while grey:
    cell = grey.pop()
    r,c = cell
    d,p = shortest[cell]
    risk = map[r][c]
    t = d + risk
    add = []
    for c in neighbours(*cell):
        go = c not in shortest
        if go:
            pass
        else:
            cd,_ = shortest[c]
            if cd > t:
                go = True
        if go:
            add.append(c)
    if add:
        newshortest = (t, p + [cell])
        for c in add:
            grey.add(c)
            shortest[c] = newshortest

print(f"lowest total risk of a path top-left to bottom-right (answer one): {shortest[0,0][0]}")
