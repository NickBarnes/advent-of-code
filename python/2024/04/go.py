diags = set(intgrid.all_dirs.values()) - set(intgrid.ortho_dirs.values())

def check(grid, p, dp, s, n):
    if n == len(s):
        return True
    if grid.get(p) == s[n]:
        return check(grid, p+dp, dp, s, n+1)
    return False

def cross(grid, p, dp, s):
    """Returns True if s appears in the grid starting at `p`, in
    the direction `dp`, and also, crossing itself at the first
    letter, rotated 90 degrees clockwise."""

    if check(grid, p, dp, s, 0):
        dpc = dp.cw()
        if check(grid, p+dp-dpc, dpc, s, 0):
            return True
    return False

def count(grid, s):
    return sum(1 for p in grid for dp in intgrid.all_dirs.values()
               if check(grid, p, dp, s, 0))

def crosses(grid, s):
    return sum(1 for p in grid for dp in diags
               if cross(grid, p, dp, s))
    
def go(input):
    grid = intgrid.IntGrid(parse.lines(input))
    print("part 1 (XMASes found):", count(grid,'XMAS'))
    print("part 2 (X MASes found):", crosses(grid,'MAS'))
