dirs = {'R':intgrid.V2(1,0),
        'L':intgrid.V2(-1,0),
        'U':intgrid.V2(0,-1),
        'D':intgrid.V2(0,1)}

def path(wire):
    p = intgrid.V2(0,0)
    q = {}
    j = 0
    for d,n in wire:
        dp = dirs[d]
        for i in range(n):
            j += 1
            p += dp
            if p not in q:
                q[p] = j
    return q

def go(input):
    lines = parse.lines(input)
    assert len(lines) == 2
    wires = [[(s[0],int(s[1:]))
              for s in line.split(',')]
             for line in lines]

    assert all(all(dir[0] in 'RLUD' for dir in wire) for wire in wires)
    path1 = path(wires[0])
    path2 = path(wires[1])
    least_sum = len(path1) + len(path2)
    dist = len(path1)
    for p in path1:
        if p in path2:
            d = len(p)
            s = path1[p] + path2[p]
            if d < dist:
                dist = d
            if s < least_sum:
                least_sum = s
    print("part 1 (closest intersection):", dist)
    print("part 2 (least sum):", least_sum)

