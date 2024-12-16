def go(input):
    lines = parse.lines(input)
    grid = intgrid.IntGrid(parse.lines(input))
    start = grid.find_only('S')
    end = grid.find_only('E')

    # Find all the shortest paths to everywhere. A-star would probably
    # be quicker.
    grey = []
    shortest = {}             # (p,dp) -> lowest cost
    back = defaultdict(set)   # (p,dp) -> set of tiles on best paths
    winner = 1000 * grid.area

    # record that we can get to `k` from `oldk` at `cost`
    def add (oldk, k, cost):
        nonlocal winner
        c = grid.get((k[0]))
        if c == '#':
            return
        if c == 'E' and cost < winner:
            winner = cost
        if k not in shortest or shortest[k] > cost: # new shortest route
            shortest[k] = cost
            back[k] = back[oldk] | {k[0]}
            heapq.heappush(grey, (cost, k))
        elif shortest[k] == cost: # alternative route, same cost
            back[k] |= back[oldk]

    add((start, intgrid.ortho_dirs['>']), (start, intgrid.ortho_dirs['>']), 0)

    while grey:
        cost,k = heapq.heappop(grey)
        if cost > winner: # everything left on heap loses
            break
        if shortest[k] < cost: # already got here for less
            continue
        p, dp = k
        add (k, (p+dp, dp), cost+1)
        add (k, (p, dp.cw()), cost+1000)
        add (k, (p, dp.ccw()), cost+1000)

    print("part 1 (winning reindeer score):", winner)

    # Could come at final square from several directions
    winning_directions = [dp
                          for ((p,dp),c) in shortest.items()
                          if p == end and c == winner]
    # all best tiles
    best = set.union(*(back[(end, dp)] for dp in winning_directions))
    print("part 2 (number of best spots):", len(best))
    # map of best spots
    grid.set_all(best, 'O')
    print(grid.show())
    
