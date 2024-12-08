import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

depths = [[int(c) for c in l.strip()] for l in open(input,'r').readlines()]
rows = len(depths)
cols = len(depths[0])
depths = [[10] * (cols+2)] + [[10] + r + [10] for r in depths] + [[10] * (cols+2)]
lows = [(r,c) for r in range(1,rows+1) for c in range(1,cols+1)
        if (depths[r][c] < depths[r+1][c] and
            depths[r][c] < depths[r-1][c] and
            depths[r][c] < depths[r][c+1] and
            depths[r][c] < depths[r][c-1])]
risk_total = sum(1 + depths[r][c] for (r,c) in lows)
print(f"risk total (answer 1): {risk_total}")

# cell -> low point for each cell in a basin
basin = {l:l for l in lows}

# cell -> colour during colouring: 1 is white, 2 is grey, 3 is black
colour = {(r,c):1 for r in range(rows+2) for c in range(cols+2)}

# grey set
grey = set(lows)
for g in grey:
    colour[g] = 2

# look at a neighbour of a grey cell.
def touch(r,c,b):
    if colour[(r,c)] == 1: # white
        if depths[r][c] < 9:
            basin[(r,c)] = b
            colour[(r,c)] = 2
            grey.add((r,c))
        else: # highlands straight to black, no basin
            colour[(r,c)] = 3
        
# marking algorithm
while grey:
    r,c = grey.pop()
    colour[(r,c)] = 3
    b = basin[(r,c)]
    touch(r+1,c,b)
    touch(r-1,c,b)
    touch(r,c+1,b)
    touch(r,c-1,b)

# invert basin map to find basins
basin_cells = {b:[] for b in set(basin.values())}
for c,b in basin.items():
    basin_cells[b].append(c)
print(f"{len(basin_cells)} basins")
basin_lens=sorted([(len(v),k) for k,v in basin_cells.items()], reverse=True)

import math
product=math.prod(l for l,_ in basin_lens[:3])
print(f"product of largest three basin sizes (answer two): {product}")
