# Generalised solution to a robot pushing arbitrarily-shaped boxes
# around a warehouse (as long as each character of a box uniquely
# identifies the box shape and the character's position within it).

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

# Relative coordinates of other parts of a box, given a box character.
boxes = {'O': [],
         '[' : [(1,0)],
         ']' : [(-1,0)],
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

    # If it's possible for the robot to move from x,y to x+dx,y+dy,
    # then do so.
    def push(x,y,dx,dy):
        movers = {}
        grey = {(x,y)}
        def add(x,y):
            if (x,y) not in movers:
                grey.add((x,y))
        while grey:
            mx,my = grey.pop()
            assert (mx,my) in grid
            movers[(mx,my)] = grid[(mx,my)]
            cx,cy = mx+dx,my+dy
            c = grid.get((cx,cy))
            if c is None: # empty space, can move
                continue
            elif c == '#': # wall: entire move is cancelled
                return x,y
            else:
                assert c in boxes
                add(cx,cy)
                for px,py in boxes[c]:
                    add(cx+px,cy+py)
        for mx,my in movers:
            del grid[(mx,my)]
        for mx,my in movers:
            grid[(mx+dx,my+dy)] = movers[(mx,my)]
        return x+dx,y+dy

    # part 1
    x,y = rx,ry
    for dx,dy in insns:
        x,y = push(x,y,dx,dy)
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
        x,y = push(x,y,dx,dy)
    print("part 2 (GPS total for larger warehouse):",
          sum(100*j+i for (i,j) in grid if grid[(i,j)] == '['))
    print('\n'.join(''.join(grid.get((i,j),' ') for i in range(width))
                    for j in range(height)))
