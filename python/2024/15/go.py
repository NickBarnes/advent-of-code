dirs = {'^': (0,-1),
        'v': (0,1),
        '<': (-1,0),
        '>': (1,0),
    }

scaled = {'#':'##',
          'O':'[]',
          '@':'@.',
          '.':'..',
        }

def go(input):
    warehouse,insns = parse.sections(input)
    grid = {(i,j):c
            for j,l in enumerate(warehouse)
            for i,c in enumerate(l)
            if c != '.'}
    height = len(warehouse)
    width = len(warehouse[0])

    insns = [dirs[c] for c in ''.join(insns) if c in dirs]

    robots = set(p for p in grid if grid[p] == '@')
    assert len(robots) == 1
    rx,ry = robots.pop()

    def move(x1,y1,x2,y2):
        assert (x2,y2) not in grid
        grid[(x2,y2)] = grid[(x1,y1)]
        del grid[(x1,y1)]

    # part 1
    x,y = rx,ry
    for dx,dy in insns:
        tx,ty = x+dx, y+dy
        while grid.get((tx,ty)) == 'O':
            tx,ty = tx+dx, ty+dy
        if (tx,ty) not in grid: # move chain
            while tx != x or ty != y:
                move(tx-dx,ty-dy,tx,ty)
                tx,ty = tx-dx, ty-dy
            x,y = x+dx,y+dy
        else:
            assert grid[(tx,ty)] == '#'

    print("part 1 (GPS total from basic warehouse):",
          sum(100*j+i for (i,j) in grid if grid[(i,j)] == 'O'))
    print('\n'.join(''.join(grid.get((i,j),' ') for i in range(width))
                    for j in range(height)))

    # scale up warehouse
    larger = [''.join(scaled[c] for c in l) for l in warehouse]
    grid = {(i,j):c
            for j,l in enumerate(larger)
            for i,c in enumerate(l)
            if c != '.'}
    width *= 2

    # part 2
    x,y = 2*rx,ry
    for dx,dy in insns:
        movers = set()
        grey = {(x,y)}
        moving = True
        while grey:
            mx,my = grey.pop()
            assert (mx,my) in grid
            movers.add((mx,my))
            cx,cy=mx+dx,my+dy
            if grid.get((cx,cy)) == '#': # wall: entire move is cancelled
                grey,moving = set(), False
            elif grid.get((cx,cy)) == '[' and dx != -1:
                grey.add((cx,cy))
                grey.add((cx+1,cy))
            elif grid.get((cx,cy)) == ']' and dx != 1:
                grey.add((cx,cy))
                grey.add((cx-1,cy))
        if moving:
            move = {(mx,my):grid[(mx,my)] for (mx,my) in movers}
            for mx,my in move:
                del grid[(mx,my)]
            for mx,my in move:
                grid[(mx+dx,my+dy)] = move[(mx,my)]
            x,y = x+dx,y+dy
    print("part 2 (GPS total for larger warehouse):",
          sum(100*j+i for (i,j) in grid if grid[(i,j)] == '['))
    print('\n'.join(''.join(grid.get((i,j),' ') for i in range(width))
                    for j in range(height)))
