def go(input):
    grid = intgrid.IntGrid(parse.digits(input))
    starts = set(p for p in grid if grid.get(p) == 0)

    def uphill(p):
        val = grid.get(p)
        for dp in intgrid.ortho_dirs.values():
            newp = p+dp
            if grid.get(newp) == val+1:
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

    
        
                

