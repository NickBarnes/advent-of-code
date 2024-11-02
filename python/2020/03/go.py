# Template for AoC daily solution. To add to imports, see
# util/__init__.py.

def count(grid, dx, dy):
    i, j = 0,0
    trees = 0
    while j < len(grid):
        if grid[j][i] != '.':
            trees += 1
        j += dy
        i = (i + dx) % len(grid[0])
    return trees

def go(input):
    grid = parse.chars(input)
    print("part 1:", count(grid, 3, 1))
    print("part 2:", misc.prod(count(grid, dx, dy) for dx,dy in
                               [(1,1),(3,1),(5,1),(7,1),(1,2)]))
    
