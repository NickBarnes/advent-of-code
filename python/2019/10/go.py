def direction(a1,a2):
    assert a1 != a2
    dx,dy = a2.x-a1.x, a2.y-a1.y
    if dx != 0 != dy:
        g = math.gcd(dx,dy)
        dx,dy = dx/g, dy/g
    elif dy == 0:
        dx = -1 if dx < 0 else 1
    else:
        assert dx == 0
        dy = -1 if dy < 0 else 1
    return intgrid.V2(dx,dy)
        

def go(input):
    grid = intgrid.IntGrid(parse.lines(input))
    views = defaultdict(set)
    for a1 in grid:
        count = 0
        for a2 in grid:
            if a1 == a2: continue
            dp = direction(a1,a2)
            p = a1 + dp
            while p != a2:
                if p in grid:
                    break
                p += dp
            else:
                count += 1
        
        views[count].add(a1)
    best_asteroid_views = max(views)
    best_asteroids = views[best_asteroid_views]
    assert len(best_asteroids) == 1
    best_asteroid = best_asteroids.pop()
    print("part 1 (best asteroid location):", best_asteroid)

    dirs = defaultdict(dict)
    for a in grid:
        if a != best_asteroid:
            dir = direction(best_asteroid, a)

            # atan2 runs from -pi to pi anticlockwise from the
            # negative x axis on conventional axes, whereas we want an
            # angle running clockwise from the negative y axis, on
            # this inverted y axis, so we need to rotate clockwise
            # dx,dy to dy,-dx.
            if dir.x == 0 and dir.y < 0:
                angle = -math.pi
            else:
                angle = math.atan2(-dir.x, dir.y)
            dp = a - best_asteroid
            dist = abs(dp.x) + abs(dp.y)
            assert dist not in dirs[angle]
            dirs[angle][dist] = a
    count = 0
    while count < 200 and dirs:
        for angle in sorted(dirs):
            line = dirs[angle]
            dist = min(line)
            a = line[dist]
            del line[dist]
            if not line:
                del dirs[angle]
            count += 1
            if count == 200:
                break
    assert AoC.testing or count == 200
    if count == 200:
        print("part 2 (200th asteroid vaporized):", a)
