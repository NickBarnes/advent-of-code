import re
import sys
import heapq

# Could replace this with something from util/

class Walk:
    def __init__(self, good, inc):
        self.good = good
        self.inc = inc

    def walk(self, grid, start):
        rows = len(grid)
        cols = len(grid[0])

        def neighbours(i,j):
            if i > 0: yield (i-1,j)
            if i < rows-1: yield (i+1,j)
            if j > 0: yield (i,j-1)
            if j < cols-1: yield (i,j+1)

        grey = [(0, start)]
        far = {start: 0}

        while grey:
            d, pos = heapq.heappop(grey)
            r,c = pos
            if far[pos] < d: # already seen at shorter distance
                continue
            d += self.inc(pos)
            for n in neighbours(r, c):
                if self.good(pos, n) and (n not in far or far[n] > d):
                    heapq.heappush(grey, (d, n))
                    far[n] = d
        return far

def go(input):
    map = [[int(r) for r in l] for l in parse.lines(input)]

    def best(map):
        # Lowest total on path from lower right to upper right.
        walker = Walk(lambda _,__: True, lambda pos: map[pos[0]][pos[1]])
        risks = walker.walk(map, (len(map)-1,len(map[0])-1))
        return risks[(0,0)]

    smallbest = best(map)
    print(f"part 1 (lowest total path risk): {smallbest}")

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

    print(f"part 2 (lowest total path risk on enlarged map): {bigbest}")
