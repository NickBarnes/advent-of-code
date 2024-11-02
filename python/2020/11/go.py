# How many seats adjacent to (r,c) are occupied?

def close(grid, r, c):
    occupied = 0
    for dr in range(-1,2):
        for dc in range(-1, 2):
            if dr == dc == 0:
                continue
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]):
                continue
            if grid[nr][nc] == '#':
                occupied += 1
    return occupied

# How many seats visible from (r,c) are occupied?

def seen(grid, r, c):
    occupied = 0
    for dr in range(-1,2):
        for dc in range(-1, 2):
            if dr == dc == 0:
                continue
            nr,nc = r,c
            while True:
                nr += dr
                nc += dc
                if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]):
                    break
                if grid[nr][nc] == '.':
                    continue
                elif grid[nr][nc] == '#':
                    occupied += 1
                    break
                else: # stop on empty seat
                    break
    return occupied

# using the `counter` function to count occupied seats, and vacating seats if they
# have a count of `limit` or more, iterate the state of cell `(r,c)`.

def itercell(grid,r,c,counter,limit):
    state = grid[r][c]
    if state == '.':
        return '.'
    n = counter(grid, r, c)
    if state == 'L' and n == 0:
        return '#'
    elif state == '#' and n >= limit:
        return 'L'
    return state

# Given a grid, a counter function, and a limit, return an iterated grid.

def iter (grid, counter, limit):
    return tuple(tuple(itercell(grid,r,c,counter,limit) for c in range(len(grid[0])))
                 for r in range(len(grid)))

def run(grid, counter, limit):
    grid = [r[:] for r in grid] # fresh copy of grid
    rounds = 0
    while True:
        newgrid = iter(grid, counter, limit)
        if newgrid == grid:
            return rounds, grid
        rounds += 1
        grid = newgrid

def occupied(grid):
    return sum(sum(1 for state in r if state == '#') for r in grid)

def go(input):
    grid = parse.chars(input)
    rounds, newgrid = run(grid, close, 4)
    print(f"part 1 (counting immediate neighbours only with limit 4): {occupied(newgrid)}")
    rounds, newgrid = run(grid, seen, 5)
    print(f"part 2 (counting visible seats with limit 5): {occupied(newgrid)}")
    
