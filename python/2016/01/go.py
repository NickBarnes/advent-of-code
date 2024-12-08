def go(input):
    x, y = 0,0
    dx, dy = 0, 1
    visited = set() # all visited intersections
    twice = None    # first intersection visited twice

    for insn in input.split(', '):
        assert insn[0] in 'LR'
        if insn[0] == 'L':
            dx, dy = -dy, dx
        elif insn[0] == 'R':
            dx, dy = dy, -dx

        dist = int(insn[1:])
        for i in range(dist):
            if twice is None:
                if (x,y) in visited:
                    twice = (x,y)
                else:
                    visited.add((x,y))
            x, y = x + dx, y + dy

    print("part 1 (distance to end of instructions):", abs(x)+abs(y))
    print("part 2 (distance to first intersection visited twice):",
          abs(twice[0])+abs(twice[1]))
