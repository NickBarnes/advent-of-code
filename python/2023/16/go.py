def beam(grid, pd):
    energized = defaultdict(set)
    while pd:
        newpd = []
        for p,d in pd:
            if p not in grid:
                continue
            if d in energized[p]:
                continue
            energized[p].add(d)
            c = grid[p]
            if c == '/':
                ds = [(-d[1],-d[0])]
            elif c == '\\':
                ds = [(d[1],d[0])]
            elif c == '-' and d[1]:
                ds = [(-1,0),(1,0)]
            elif c == '|' and d[0]:
                ds = [(0,-1),(0,1)]
            else:
                ds = [d]
            newpd += [(newp,d) for d in ds if (newp := (p[0]+d[0],p[1]+d[1])) in grid]
        pd = newpd
    return len(energized)

def max_beam(grid, rows, cols):
    mleft = max(beam(grid, [((0,j),(1,0))]) for j in range(rows))
    mright = max(beam(grid, [((cols-1,j),(-1,0))]) for j in range(rows))
    mtop = max(beam(grid, [((i,0),(0,1))]) for i in range(cols))
    mbottom = max(beam(grid, [((i,rows-1),(0,-1))]) for i in range(cols))
    return max(mleft, mright, mtop, mbottom)

def go(input):
    lines = parse.lines(input)
    grid = {(i,j):c for j,row in enumerate(lines) for i,c in enumerate(row)}
    print(beam(grid, [((0,0),(1,0))]))
    print(max_beam(grid, len(lines), len(lines[0])))
