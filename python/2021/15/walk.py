import heapq

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
