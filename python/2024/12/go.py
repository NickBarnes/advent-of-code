# Find the set of cells in an orthogonally-connected region of a grid
# which all have the same grid value.

def region(grid, p, xlim, ylim):
    grey = {p}
    region = {p}
    seen = {p}

    id = grid[p]
    neighbours = graph.grid(xlim, ylim)
    while grey:
        p = grey.pop()
        for n in neighbours(p):
            if n not in seen:
                seen.add(n)
                if grid[n] == id:
                    grey.add(n)
                    region.add(n)
    return region

# Find all the orthogonally-connected single-value regions of a grid.

def all_regions(grid, xlim, ylim):
    white = set(grid)
    regions = []
    while white:
        p = white.pop()
        found = region(grid, p, xlim, ylim)
        regions.append((grid[p], found))
        white = white - found
    return regions

# Find the set of edge segments of a region.  Each edge segment is
# (x,y,dx,dy) for x,y in the region and dx,dy pointing out.

def perimeter(region):
    total = set()
    for x,y in region:
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            if (x+dx,y+dy) not in region:
                total.add((x,y,dx,dy))
    return total

# Given the set of edge segments for a region, find the set of
# edges. Each edge is (x,y,ex,ey,count) for x,y in the region, ex,ey
# pointing along the edge, and count the number of segments in the
# edge.

def edges(segments):
    found = set()
    segments = segments.copy()
    while segments:
        x,y,dx,dy = segments.pop()
        count = 0
        # look clockwise
        nx,ny,ex,ey = x,y,-dy,dx
        while (nx+ex,ny+ey,dx,dy) in segments:
            nx,ny = nx+ex,ny+ey
            segments.remove((nx,ny,dx,dy))
            count += 1
        # look anti-clockwise
        nx,ny,ex,ey = x,y,-ex,-ey
        while (nx+ex,ny+ey,dx,dy) in segments:
            nx,ny = nx+ex,ny+ey
            segments.remove((nx,ny,dx,dy))
            count += 1
        found.add((x,y,ex,ey,count))
    return found

def go(input):
    chars = parse.chars(input)
    xlim, ylim = len(chars[0]), len(chars)
    grid = {(x,y):chars[y][x]
            for y in range(ylim)
            for x in range(xlim)}

    regions = all_regions(grid, xlim, ylim)

    cost1,cost2 = 0,0
    for id, cells in regions:
        perim = perimeter(cells)
        sides = edges(perim)
        cost1 += len(perim) * len(cells)
        cost2 += len(sides) * len(cells)

    print("part 1 (fencing cost):", cost1)
    print("part 2 (fencing cost with discount):", cost2)
    
        
    
