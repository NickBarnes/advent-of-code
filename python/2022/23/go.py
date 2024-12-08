# The directions checked for each possible move. The middle direction
# is the one taken.

moves = [((-1,-1),(0,-1),(1,-1)),
         ((-1,1),(0,1),(1,1)),
         ((-1,-1),(-1,0),(-1,1)),
         ((1,-1),(1,0),(1,1))]

def go(input):
    global moves
    elves = {(x,y) for y,l in enumerate(parse.lines(input)) for x in range(len(l)) if l[x] == '#'}

    round = 0
    while True:
        prop = {} # destination -> current location of proposer
        act = {} # location -> destination
        for x,y in elves:
            # default is not to move
            act[(x,y)] = (x,y)
            neighbours = sum(1 for dx in range(-1,2) for dy in range(-1, 2) if (x+dx,y+dy) in elves)
            if neighbours == 1: # lonely elves don't move
                continue
            for move in moves:
                seen = sum(1 for dx,dy in move if (x+dx,y+dy) in elves)
                if seen != 0: # somebody there, consider next move direction
                    continue
                nx,ny = x+move[1][0],y+move[1][1]
                if (nx,ny) in prop: # already proposed
                    act[prop[(nx,ny)]] = prop[(nx,ny)] # proposer can't move
                else:
                    prop[(nx,ny)] = (x,y) # propose
                    act[(x,y)] = (nx,ny)  # assume we're going to move
                break

        # how many elves are moving?
        moved = sum(1 for e in elves if act[e] != e)
        # move all the elves
        elves = {act[elf] for elf in elves}
        round += 1
        if round == 10:
            # part 1
            minx = min(x for x,y in elves)
            maxx = max(x for x,y in elves)
            miny = min(y for x,y in elves)
            maxy = max(y for x,y in elves)
            free = (maxx-minx+1)*(maxy-miny+1)-len(elves)
            print(f"part 1 (free spots in bounding box after {round} rounds): {free}")
        if moved == 0:
            # part 2
            print(f"part 2 (round when no elves move): {round}")
            break
        # rotate the moves for the next round
        moves = moves[1:]+moves[:1]
