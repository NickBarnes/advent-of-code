robot_re=re.compile(r'^p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)$')

def go(input):
    robots = [robot_re.match(l) for l in parse.lines(input)]
    assert all(robots)
    robots = [tuple(int(s) for s in r.groups()) for r in robots]
    testing = len(robots) < 20
    width,height = (11,7) if testing else (101,103)
    qw,qh = width // 2, height // 2

    counts = Counter()
    for xi,yi,xv,yv in robots:
        x,y = (xi + 100 * xv) % width, (yi + 100 * yv) % height
        if x == qw or y == qh: # mid-line
            continue
        quadrant = (x < qw, y < qh)
        counts[quadrant] += 1
    print("part 1 (total safety factor after 100 seconds):",
          misc.prod(counts.values()))

    if not testing:
        t = 0
        while True:
            t += 1
            robots = [((x+vx) % width,(y+vy) % height,vx,vy)
                      for (x,y,vx,vy) in robots]
            robotmap = set((x,y) for (x,y,vx,vy) in robots)
            adjacents = sum(1 for x,y in robotmap
                            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))
                            if (x+dx,y+dy) in robotmap)
            if adjacents > len(robots):
                # rule of thumb: average robot adjacent to at least one
                # other.
                print(f"part 2 (easter egg picture time): {t}")
                print('\n'.join(''.join('*' if (i,j) in robotmap else ' '
                                        for i in range(width))
                                for j in range(height)))
                break
            
        

        
        
        
    
