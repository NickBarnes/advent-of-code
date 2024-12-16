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
    shortest = {}             # (x,y,dx,dy) -> lowest cost
    back = defaultdict(set)   # (x,y,dx,dy) -> set of tiles on best paths
    winner = 1000 * len(grid)

    # record that we can get to `k` from `oldk` at `cost`
    def add (oldk,k,cost):
        nonlocal winner
        c = grid.get((k[0],k[1]))
        if c == '#':
            return
        if c == 'E' and cost < winner:
            winner = cost
        if k not in shortest or shortest[k] > cost: # new shortest route
            shortest[k] = cost
            back[k] = back[oldk] | {k}
            heapq.heappush(grey, (cost, k))
        elif shortest[k] == cost: # alternative route, same cost
            back[k] |= back[oldk]

    add((sx,sy,1,0),(sx,sy,1,0),0)

    while grey:
        cost,k = heapq.heappop(grey)
        if cost > winner: # everything left on heap loses
            break
        if shortest[k] < cost: # already got here for less
            continue
        x,y,dx,dy = k
        add (k,(x+dx,y+dy,dx,dy),cost+1)
        add (k,(x,y,-dy,dx),cost+1000)
        add (k,(x,y,dy,-dx),cost+1000)

    print("part 1 (winning reindeer score):", winner)

    # Could come at final square from several directions
    winning_directions = [(dx,dy)
                          for ((x,y,dx,dy),c) in shortest.items()
                          if x == ex and y == ey and c == winner]
    # all best tiles
    best = set((x,y)
               for dx,dy in winning_directions
               for x,y,_,_ in back[(ex,ey,dx,dy)])
    print("part 2 (number of best spots):", len(best))
    # map of best spots
    print('\n'.join(''.join('O' if (i,j) in best else 
                            '#' if grid.get((i,j)) == '#' else
                            ' ' for i in range(width))
                    for j in range(height)))
    
