def go(input):
    grid = parse.digits(input)

    xlim, ylim = len(grid[0]), len(grid)
    map = {(x,y):grid[y][x] for x in range(xlim) for y in range(ylim)}
    starts = [(x,y) for x,y in map if map[(x,y)] == 0]

    def uphill(p):
        x,y = p
        val = map[p]
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (dx and dy) or (dx == dy == 0): # orthogonal only
                    continue
                newp = (x+dx, y+dy)
                if map.get(newp) == val+1:
                    yield newp
    
    score = 0
    for start in starts:
        ps,val = {start,},0
        while val < 9:
            ps = {newp for p in ps for newp in uphill(p)}
            val += 1
            if not ps:
                break
        score += len(ps)
    print("part 1 (total of peaks reachable from trailheads):", score)

    score = 0
    for start in starts:
        paths,val = [[start]], 0
        while val < 9:
            paths = [path[:]+[p] for path in paths for p in uphill(path[-1])]
            val += 1
            if not paths:
                break
        score += len(paths)
    print("part 2 (total paths to peaks reachable from trailheads):", score)

    
        
                

