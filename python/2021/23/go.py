# destination columns

col = {'A': 3,
       'B': 5,
       'C': 7,
       'D': 9,
}

cost = {'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
}

def solve(puzzle):
    grid = [l.rstrip() for l in puzzle.rstrip().split('\n')] # keep left spaces
    homes = {}
    for c in 'ABCD':
        homes[c] = [row[col[c]] for row in grid[2:-1]]
    top=[c for c in grid[1]]

    # possible parking spaces along the top
    slots = [1,2,4,6,8,10,11]
    
    def done(homes):
        return all(all(d == c for d in homes[c]) for c in 'ABCD')

    # can we get from column A to column B along the top?
    def clear(colA, colB, top):
        return all(top[x] == '.' for x in range(min(colA, colB)+1, max(colA, colB)))

    # is the home column for 'c' ready to move into?
    def open_home(c, homes):
        return all(k == c or k == '.' for k in homes[c])

    # index of first occupied spot in a "home" column
    def top_spot(c, homes):
        if homes[c][0] != '.':
            return 0
        return max(i+1 for i in range(len(homes[c])) if homes[c][i]=='.')
    
    # handy for debugging
    def show(homes, top):
        print(''.join(top[1:-1]))
        print('\n'.join(('  '+' '.join(homes[c][i] for c in 'ABCD')) for i in range(len(homes['A']))))

    cache = {}

    def best(state):
        # cost to get done from here
        homes, top = state
        key = (tuple(tuple(homes[c]) for c in 'ABCD'), tuple(top))
        if key in cache:
            return cache[key]
        # any we can move home, from the top, we just do so.
        easy_cost = 0
        moving = True
        while moving: # check all the spots repeatedly until we don't move any of them.
            moving = False
            for i in slots:
                c = top[i]
                if c != '.' and clear(i,col[c], top) and open_home(c, homes):
                    moving = True
                    j = top_spot(c, homes)
                    dist = abs(i - col[c]) + j
                    move_cost = cost[c] * dist
                    easy_cost += move_cost
                    top[i] = '.'
                    homes[c][j-1] = c
        if done(homes):
            cache[key] = easy_cost
            return easy_cost

        # We've not finished and there's nothing ready to retire in any resting slot, so we must have to
        # move something out of a home to a resting slot.
        lowest = 1e9
        for k in 'DCBA':
            if not open_home(k, homes): # something to move out
                j = top_spot(k, homes) # move out 
                c = homes[k][j]
                # and somewhere to move it
                for slot in slots:
                    if not (top[slot] == '.' and clear(slot, col[k], top)):
                        continue
                    dist = abs(col[k]-slot) + j + 1
                    move_cost = cost[c] * dist
                    new_homes = {c: homes[c][:] for c in 'ABCD'}
                    new_homes[k][j] = '.'
                    new_top = top[:]
                    new_top[slot] = c
                    ans = best((new_homes, new_top))
                    if ans + move_cost < lowest:
                        lowest = ans + move_cost
        lowest += easy_cost
        cache[key] = lowest
        return lowest

    return best((homes,top))

def go(input):
    puzzles = input.split('\n\n')
    for i, puzzle in enumerate(puzzles, start=1):
        cost = solve(puzzle)
        print(f"part {i} (lowest cost solution for puzzle {i}): {cost}")
