def all_dirs():
    for dx in range(-1,2):
        for dy in range(-1,2):
            if dx or dy:
                yield dx,dy

def diags():
    for dx in range(-1,2):
        for dy in range(-1,2):
            if dx and dy:
                yield dx,dy

def check(grid, x, y, dx, dy, s, n):
    if n == len(s):
        return True
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] == s[n]:
        return check(grid, x+dx, y+dy, dx, dy, s, n+1)
    return False

def cross(grid, x, y, dx, dy, s):
    if check(grid, x, y, dx, dy, s, 0):
        cross_dx, cross_dy = -dy, dx # counter-clockwise
        if check(grid, x+dx-cross_dx, y+dy-cross_dy, cross_dx, cross_dy, s, 0):
            return True
        cross_dx, cross_dy = dy, -dx # clockwise
        if check(grid, x+dx-cross_dx, y+dy-cross_dy, cross_dx, cross_dy, s, 0):
            return True
    return False

def count(grid, s):
    return sum(1
               for y in range(len(grid))
               for x in range(len(grid[0]))
               for dx,dy in all_dirs()
               if check(grid, x, y, dx, dy, s, 0))

def crosses(grid, s):
    # every cross will be counted twice. Could do better.
    count = sum(1
                for y in range(len(grid))
                for x in range(len(grid[0]))
                for dx,dy in diags()
                if cross(grid, x, y, dx, dy, s))
    assert count % 2 == 0
    return count // 2
    
def go(input):
    grid = parse.lines(input)
    print(count(grid,'XMAS'))
    print(crosses(grid,'MAS'))
    
