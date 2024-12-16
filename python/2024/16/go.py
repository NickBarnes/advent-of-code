def go(input):
    lines = parse.lines(input)
    grid = {(i,j): c
            for j,l in enumerate(lines)
            for i,c in enumerate(l)
            if c != '.'}
    width,height = len(lines[0]),len(lines)

    starts = [p for p,c in grid.items() if c == 'S']
    assert len(starts) == 1
    ends = [p for p,c in grid.items() if c == 'E']
    assert len(ends) == 1
    sx,sy = starts[0]
    ex,ey = ends[0]

    # Find all the shortest paths to everywhere. A-star would probably
    # be quicker.

    grey = []
    shortest = {}
    back = defaultdict(set)

    # record that we can get to `k` (at p) from `oldk` at `cost`
    def add (oldk,k,cost):
        if grid.get((k[0],k[1])) == '#':
            return
        if k not in shortest or shortest[k] > cost: # new shortest route
            shortest[k] = cost
            back[k] = back[oldk] | {oldk,k}
            heapq.heappush(grey, (cost,k))
        if shortest[k] == cost: # alternative route, same cost
            back[k] |= back[oldk] | {oldk,k}

    add((sx,sy,1,0),(sx,sy,1,0),0)

    while grey:
        cost,k = heapq.heappop(grey)
        if shortest[k] < cost: # already got here for less
            continue
        x,y,dx,dy = k
        add (k,(x+dx,y+dy,dx,dy),cost+1)
        add (k,(x,y,-dy,dx),cost+1000)
        add (k,(x,y,dy,-dx),cost+1000)
    
    total_costs = sorted((c,dx,dy) for ((x,y,dx,dy),c) in shortest.items()
                         if x == ex and y == ey)
    print("part 1 (winning reindeer score):",
          total_costs[0][0])

    # winning direction
    bestdx,bestdy = total_costs[0][1],total_costs[0][2]
    # all best tiles
    best = set((x,y) for x,y,_,_ in back[(ex,ey,bestdx,bestdy)])
    print("part 2 (number of best spots):", len(best))
    # map of best spots
    print('\n'.join(''.join('O' if (i,j) in best else 
                            '#' if grid.get((i,j)) == '#' else
                            ' ' for i in range(width))
                    for j in range(height)))
    
