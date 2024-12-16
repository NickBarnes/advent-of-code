def go(input):
    grid = intgrid.IntGrid(parse.lines(input))
    guard = grid.find_only('^')
    obstacles = set(grid.find('#'))
    assert len(obstacles) > 1

    def follow(p, dp, extra_obstacle=None):
        assert extra_obstacle not in obstacles
        path = set()
        loop = False
        while 0 <= p.x < grid.width and 0 <= p.y < grid.height:
            key = (p, dp)
            if key in path:
                loop = True
                break
            path.add((p, dp))
            n = p+dp
            if n not in obstacles and (extra_obstacle is None or n != extra_obstacle):
                # continue
                p = n
            else:
                # turn right
                dp = dp.cw()
        return loop, path

    loop, part1_path = follow(guard, intgrid.ortho_dirs['^'])
    assert not loop
    posns = set(p for (p,dp) in part1_path)
    print(f"part 1 (steps until the guard leaves): {len(posns)}")

    posns.remove(guard) # don't put obstacle at start point
    good = sum(1 for test in posns if follow(guard,intgrid.ortho_dirs['^'],test)[0])
    print(f"part 2 (good spots for a loop-causing obstacle): {good}")
