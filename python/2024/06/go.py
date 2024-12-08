def go(input):
    chars = parse.chars(input)
    xmax, ymax = len(chars[0]), len(chars)

    guard = [(x,y) for y in range(ymax) for x in range(xmax) if chars[y][x] == '^']
    assert len(guard) == 1
    gx, gy = guard[0]

    obstacles = set((x,y) for y in range(ymax) for x in range(xmax) if chars[y][x] == '#')
    assert len(obstacles) > 1

    def follow(x, y, dx, dy, extra_obstacle=None):
        assert extra_obstacle not in obstacles
        path = set()
        loop = False
        while 0 <= x < xmax and 0 <= y < ymax:
            key = (x, y, dx, dy)
            if key in path:
                loop = True
                break
            path.add((x, y, dx, dy))
            nx, ny = x+dx, y+dy
            if (nx,ny) not in obstacles and (nx,ny) != extra_obstacle:
                # continue
                x, y = nx, ny
            else:
                # turn right
                dx, dy = -dy, dx
        return loop, path

    loop, part1_path = follow(gx, gy, 0, -1)
    assert not loop
    posns = set((x, y) for (x,y,dx,dy) in part1_path)
    print(f"part 1 (steps until the guard leaves): {len(posns)}")

    posns.remove((gx,gy)) # don't put obstacle at start point
    good = sum(1 for test in posns if follow(gx,gy,0,-1,test)[0])
    print(f"part 2 (good spots for a loop-causing obstacle): {good}")
