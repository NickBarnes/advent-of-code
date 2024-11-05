def neighbours(x,y):
    return {(x+1,y), (x-1,y), (x,y+1), (x,y-1), (x-1,y+1), (x+1,y-1)}

# one iteration of the cellular automaton
def generate(blacks):
    for tile in set.union(*(neighbours(*t) for t in blacks)):
        n = len(neighbours(*tile) & blacks)
        if tile in blacks:
            if 0 < n < 3:
                yield tile # otherwise flip to white
        elif n == 2:
            yield tile # flip to black
            
            
    return set.union(*(neighbours(x,y) for x,y in blacks))

def go(input):
    flips = Counter()
    for flip in parse.lines(input):
        x,y = 0,0
        i = 0
        while i < len(flip):
            if flip.startswith('e',i):
                x += 1
                i += 1
            elif flip.startswith('w',i):
                x -= 1
                i += 1
            elif flip.startswith('ne', i):
                y += 1
                i += 2
            elif flip.startswith('nw', i):
                y += 1
                x -= 1
                i += 2
            elif flip.startswith('se', i):
                y -= 1
                x += 1
                i += 2
            elif flip.startswith('sw', i):
                y -= 1
                i += 2
        flips[(x,y)] += 1
    blacks = set(loc for loc,n in flips.items() if n % 2 == 1)
    print("part 1 (tiles left black-side up):", len(blacks))

    for gen in range(100):
        blacks = set(generate(blacks))
    print("part 2 (tiles left black after 100 generations):", len(blacks))
