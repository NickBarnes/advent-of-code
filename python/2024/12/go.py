# Find the set of edge segments of a region.  Each edge segment is
# (x,y,dx,dy) for x,y in the region and dx,dy pointing out.

def perimeter(region):
    total = set()
    for p in region:
        for dp in intgrid.ortho_dirs.values():
            if p+dp not in region:
                total.add((p,dp))
    return total

# Given the set of edge segments for a region, find the set of
# edges. Each edge is (x,y,ex,ey,count) for x,y in the region, ex,ey
# pointing along the edge, and count the number of segments in the
# edge.

def edges(segments):
    found = set()
    segments = segments.copy()
    while segments:
        p,dp = segments.pop()
        count = 0
        # look clockwise
        n,e = p,dp.cw()
        while (n+e,dp) in segments:
            n = n+e
            segments.remove((n,dp))
            count += 1
        # look anti-clockwise
        n,e = p,dp.ccw()
        while (n+e,dp) in segments:
            n = n+e
            segments.remove((n,dp))
            count += 1
        found.add((p,dp,count))
    return found

def go(input):
    grid = intgrid.IntGrid(parse.lines(input))

    regions = grid.all_regions()

    cost1,cost2 = 0,0
    for id, cells in regions:
        perim = perimeter(cells)
        sides = edges(perim)
        cost1 += len(perim) * len(cells)
        cost2 += len(sides) * len(cells)

    print("part 1 (fencing cost):", cost1)
    print("part 2 (fencing cost with discount):", cost2)
    
        
    
