dirs = [(0,1),(0,-1),(1,0),(-1,0)]

# Gradually unfold `grid` until the distances from `start` to all
# cells in an infinite grid are predictable (by repeatedly adding
# `rows` and/or `cols`). Returns the number of unfoldings `U`, and the
# resulting shortest-distances `ranges` to (i,j,ti,tj) cells.

def unfold(grid, start, rows, cols):
    si,sj = start
    for U in range(1, 100):
        def weights(n):
            i,j,ti,tj = n
            for di,dj in dirs:
                nti, ni = divmod(ti * cols + i + di, cols)
                ntj, nj = divmod(tj * rows + j + dj, rows)
                if abs(nti) > U or abs(ntj) > U:
                    continue
                if (ni,nj) not in grid:
                    continue
                yield (ni,nj,nti,ntj),1
        ranges = walk.walk((si,sj,0,0), weights)
        # Have we reached the point of predictability?
        for i,j in grid:
            if ((ranges[(i,j,-U,-U)] != ranges[(i,j,-U+1,-U+1)] +rows+cols) or
                (ranges[(i,j,-U,U)] != ranges[(i,j,-U+1,U-1)] +rows+cols) or
                (ranges[(i,j,U,-U)] != ranges[(i,j,U-1,-U+1)] +rows+cols) or
                (ranges[(i,j,U,U)] != ranges[(i,j,U-1,U-1)] +rows+cols)):
                    break
            for k in range(-U+1,U):
                if ((ranges[(i,j,k,-U)] != ranges[(i,j,k,-U+1)] + rows) or
                    (ranges[(i,j,k,U)] != ranges[(i,j,k,U-1)] + rows) or
                    (ranges[(i,j,-U,k)] != ranges[(i,j,-U+1,k)] + cols) or
                    (ranges[(i,j,U,k)] != ranges[(i,j,U-1,k)] + cols)):
                    break
            else:
                continue
            break
        else:
            # everything matches, and is now predictable
            return U, ranges

# remove from `grid` all entries not reachable by Manhattan moves from `start`.
def eliminate(grid, start):
    si,sj = start
    def weights(n):
        i,j = n
        for di,dj in dirs:
            ni,nj = i + di, j + dj
            if (ni,nj) not in grid:
                continue
            yield (ni,nj),1
    ranges = walk.walk((si,sj), weights)
    return set(ranges)

def go(input):
    lines = parse.lines(input)
    step_counts = [[int(x) for x in line.split()]
                   for line in lines if line[0] in '123456789']
    lines = [line for line in lines if line[0] not in '123456789']
    rows = len(lines)
    cols = len(lines[0])
    grid = set((i,j) for j,line in enumerate(lines)
               for i,c in enumerate(line) if c != '#')
    starts = [(i,j) for j,line in enumerate(lines)
              for i,c in enumerate(line) if c == 'S']
    assert len(starts) == 1
    start = starts[0]

    # part 1: number of counts is the first thing on the first step-count line
    plots = [start]
    for k in range(step_counts[0][0]):
        new_plots = set()
        for i,j in plots:
            new_plots |= set(p for di,dj in dirs if (p := (i+di,j+dj)) in grid)
        plots = new_plots
    print("part 1, plots reachable with small step count:", len(plots), end='')
    if len(step_counts[0]) > 1:
        if len(plots) == step_counts[0][1]:
            print(" (correct)")
        else:
            print(" INCORRECT!")
    else:
        print()

    # eliminate anything unreachable, as it just adds to confusion!
    grid = eliminate(grid, starts[0])

    # part 2: unfold the grid infinitely, and consider larger numbers
    # of steps.
    U, ranges = unfold(grid, starts[0], rows, cols)

    # Assuming these lets the corner cell calculations go much faster.
    # See git history for the slow version without these assertions.
    assert rows == cols
    assert rows & 1

    # We are given solutions for several step counts on the test grid.
    for step_count in step_counts[1:]:
        steps = step_count[0]
        # cells with correct parity inside unfolded map
        total = sum(1 for v in ranges.values()
                    if v <= steps and (v ^ steps) & 1 == 0)
        for i,j in grid:
            for k in range(-U, U+1):
                # count cells going linearly away from the edge
                for ti,tj,mul in [(-U, k, cols),
                                  (U, k, cols),
                                  (k, -U, rows),
                                  (k, U, rows)]:
                    dist = ranges[(i,j,ti,tj)] # matching cell in edge tile
                    if dist < steps:
                        tiles = (steps - dist) // mul
                        total += tiles // 2 # alternate tiles
                        # one more if we miss and tiles is odd
                        if (dist ^ steps) & 1 == 1:
                            total += tiles & 1
            # now the corners
            for ti in (-U,U):
                for tj in (-U,U):
                    cells = 0
                    dist = ranges[(i,j,ti,tj)] + rows # cell above corner tile
                    if dist > steps:
                        continue
                    tiles = (steps - dist) // cols # tiles in this row
                    if (dist ^ steps) & 1 == 0: # hit, so first tile misses
                        hits = tiles // 2
                        total += hits * (hits + 1)
                    else: # miss, so first tile hits
                        hits = (tiles + 1) // 2
                        total += hits * hits
        print("part 2, plots reachable with unfolded map, "
              f"{steps} steps: {total}", end='')
        if len(step_count) > 1:
            if total == step_count[1]:
                print(" (correct)")
            else:
                print(" INCORRECT!")
        else:
            print()
