# Generalised solution to a robot pushing arbitrarily-shaped boxes
# around a warehouse (as long as each character of a box uniquely
# identifies the box shape and the character's position within it).

scaled = {'#':'##',
          'O':'[]',
          '@':'@.',
          '.':'..',
        }

# Relative coordinates of other parts of a box, given a box character.
boxes = {'O': [],
         '[' : [intgrid.V2(1,0)],
         ']' : [intgrid.V2(-1,0)],
        }

def go(input):
    warehouse,insns = parse.sections(input)
    grid = intgrid.IntGrid(warehouse)

    insns = [intgrid.ortho_dirs[c] for c in ''.join(insns) if c in intgrid.ortho_dirs]

    robot = grid.find_only('@')

    # If it's possible for the robot to move from p to p+dp,
    # then do so.
    def push(p, dp):
        movers = set()
        grey = {p}
        def add (v):
            if v not in movers:
                grey.add(v)
        while grey:
            m = grey.pop()
            movers.add(m)
            candidate = m+dp
            c = grid.get(candidate)
            if c is None: # empty space, can move
                continue
            elif c == '#': # wall: entire move is cancelled
                return p
            else:
                assert c in boxes
                add(candidate)
                for box in boxes[c]:
                    add(candidate+box)
        grid.move_all(movers, dp)
        return p+dp

    def score(v):
        return v.y * 100 + v.x

    # part 1
    p = robot
    for dp in insns:
        p = push(p,dp)
    print("part 1 (GPS total from basic warehouse):",
          sum(score(p) for p in grid if grid.get(p) == 'O'))
    print(grid.show())

    # scale up warehouse
    larger = [''.join(scaled[c] for c in l) for l in warehouse]
    grid = intgrid.IntGrid(larger)

    # part 2
    p = intgrid.V2(robot.x * 2, robot.y)
    for dp in insns:
        p = push(p, dp)
    print("part 2 (GPS total for larger warehouse):",
          sum(score(p) for p in grid if grid.get(p) == '['))
    print(grid.show())
