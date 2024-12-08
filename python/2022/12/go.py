import heapq

def walk(start, weights):
    """Find the shortest paths in a weighted network from `start` to all
    other nodes.

    """
    grey = [(0, start)]
    shortest = {start: 0}

    while grey:
        d, p = heapq.heappop(grey)
        if shortest[p] < d: # already seen at shorter distance
            continue
        for n,w in weights(p):
            if n not in shortest or shortest[n] > d + w:
                heapq.heappush(grey, (d + w, n))
                shortest[n] = d + w
    return shortest

def grid_neighbours(xmax, ymax, diagonal=False):
    """Return a neighbour function for a 2D grid size `xmax` by `ymax`. If
    `diagonal` then include diagonal neighbours.

    """
    def neighbours(p):
        x,y = p
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (not diagonal) and dx and dy:
                    continue
                newx = x+dx
                newy = y+dy
                if newx >= 0 and newx < xmax and newy >= 0 and newy < ymax:
                    yield newx, newy
    return neighbours

def go(input):
    chars = parse.chars(input)
    start = next((i, row.index('S')) for i, row in enumerate(chars) if 'S' in row)
    end = next((i, row.index('E')) for i, row in enumerate(chars) if 'E' in row)

    grid = {(i,j): 0 if c == 'S' else 25 if c == 'E' else ord(c)-ord('a')
            for i, row in enumerate(chars) for j,c in enumerate(row)}

    neighbours = grid_neighbours(len(chars), len(chars[0]))
    # reachability going down: may climb any amount but not descend more than 1
    def weights(a):
        for n in neighbours(a):
            if grid[a] - grid[n] <= 1: yield n,1

    shortest = walk(end, weights)

    print(f"part 1 (shortest path from start to end): {shortest[start]}")
    shortest_climb = min(v for p,v in shortest.items() if grid[p] == 0)
    print(f"part 2 (shortest path from low point to end): {shortest_climb}")
