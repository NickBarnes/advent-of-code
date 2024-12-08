def go(input):
    vents = []
    for l in parse.lines(input):
        a, arrow, b = l.split()
        assert arrow == '->'
        fx,fy = a.split(',')
        fx,fy=int(fx),int(fy)
        tx,ty = b.split(',')
        tx,ty=int(tx),int(ty)
        vents.append((fx,fy,tx,ty))
    mx = max(max(x for (x,_,_,_) in vents), max(x for (_,_,x,_) in vents))
    my = max(max(y for (_,y,_,_) in vents), max(y for (_,_,_,y) in vents))

    grid = [[0 for _ in range(my+1)] for _ in range(mx+1)]
    for ax,ay,bx,by in vents:
        if ax == bx: # vertical
            for y in range(min(ay,by),max(ay,by)+1):
                grid[ax][y] += 1
        elif ay == by: #horizontal
            for x in range(min(ax,bx),max(ax,bx)+1):
                grid[x][ay] += 1
        else: #diagonal
            pass
    if len(grid) < 50:
        for r in grid:
            print(r)

    hv = sum(1 for r in grid for c in r if c > 1)
    print(f"part 1 (horizontal/vertical spots with more than one vent): {hv}")

    for ax,ay,bx,by in vents:
        if ax != bx and ay != by: # diagonal
            n = abs(bx-ax)+1
            dx = 1 if bx > ax else -1
            dy = 1 if by > ay else -1
            for i in range(n):
                grid[ax][ay] += 1
                ax += dx
                ay += dy
    if len(grid) < 50:
        for r in grid:
            print(r)

    hvd = sum(1 for r in grid for c in r if c > 1)
    print(f"part 2 (all spots with more than one vent): {hvd}")
