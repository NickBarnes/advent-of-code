import intcode

dirs = {intgrid.V2(0,-1): 1, # north
        intgrid.V2(0,1):  2,  # south
        intgrid.V2(-1,0): 3, # west
        intgrid.V2(1,0):  4,  # east
        }


def go(input):
    ic = intcode.IntCode((int(s) for s in input.split(',')), AoC)

    start = intgrid.V2(0,0)
    p = start
    clear = {p} # map of clear squares
    wall = set()
    # let's do wall-following
    dp = intgrid.V2(0,-1) # start facing north
    inputs = intcode.LazyInputs([dirs[dp]])
    outputs = ic.outputs(inputs)
    goal = None
    seen = set()
    while True:
        if (p,dp) in seen:
            break
        seen.add((p,dp))
        out = next(outputs)
        np = p + dp
        if out == 0: # wall
            wall.add(np)
            dp = dp.cw() # turn right
        else: # clear
            assert 1 <= out <= 2 # clear or goal
            clear.add(np)
            p = np
            # wall-following: try to go left
            dp = dp.ccw()
            if out == 2: # goal
                goal = np
        inputs.append(dirs[dp])

    # show map of what we found
    assert not (wall & clear)
    assert goal
    
    # shortest path
    def neighbours(p):
        for dp in intgrid.ortho_dirs.values():
            np = p+dp
            if np not in wall:
                yield np,1

    def heuristic(p):
        return len(goal-p)
    
    shortest, path = graph.shortest_path(start, goal, neighbours, heuristic)
    print("part 1 (shortest path to oxygen system):", shortest)

    if AoC.verbose:
        minx = min(p.x for m in (wall, clear) for p in m)
        maxx = max(p.x for m in (wall, clear) for p in m)
        miny = min(p.y for m in (wall, clear) for p in m)
        maxy = max(p.y for m in (wall, clear) for p in m)
        print('\n'.join(''.join('O' if x==0 and y==0 else
                                '!' if goal and intgrid.V2(x,y) == goal else
                                'x' if intgrid.V2(x,y) in path else
                                '#' if intgrid.V2(x,y) in wall else
                                '.' if intgrid.V2(x,y) in clear else
                                ' ' for x in range(minx,maxx+1))
                        for y in range(miny, maxy+1)))
    
    tree = graph.shortest_tree(goal, neighbours)
    print("part 2 (time to fill with oxygen):",
          max(tree.values()))
