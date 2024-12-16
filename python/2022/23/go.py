# The directions checked for each possible move. The middle direction
# is the one taken.

moves = [tuple(intgrid.all_dirs[d] for d in 'r^7'),
         tuple(intgrid.all_dirs[d] for d in 'LvJ'),
         tuple(intgrid.all_dirs[d] for d in 'r<L'),
         tuple(intgrid.all_dirs[d] for d in '7>J'),
         ]

def go(input):
    global moves
    elves = intgrid.IntGrid(parse.lines(input))

    round = 0
    while True:
        prop = {} # destination -> current location of proposer
        act = {} # location -> destination
        for p in elves:
            # default is not to move
            act[p] = p
            if not any(p+dp in elves for dp in intgrid.all_dirs.values()):
                continue # lonely elves don't move
            for move in moves:
                seen = sum(1 for dp in move if p+dp in elves)
                if seen: # somebody there, consider next move direction
                    continue
                n = p + move[1]
                if n in prop: # already proposed
                    act[prop[n]] = prop[n] # proposer can't move
                else:
                    prop[n] = p # propose
                    act[p] = n  # assume we're going to move
                break

        # how many elves are moving?
        moved = sum(1 for e in elves if act[e] != e)
        # move all the elves
        for e,_ in list(elves.items()):
            if act[e] != e:
                elves.move(e,act[e])
        round += 1
        if round == 10:
            # part 1
            minx = min(e.x for e in elves)
            maxx = max(e.x for e in elves)
            miny = min(e.y for e in elves)
            maxy = max(e.y for e in elves)
            free = (maxx-minx+1)*(maxy-miny+1)-len(elves.items())
            print(f"part 1 (free spots in bounding box after {round} rounds): {free}")
        if moved == 0:
            # part 2
            print(f"part 2 (round when no elves move): {round}")
            break
        # rotate the moves for the next round
        moves = moves[1:]+moves[:1]
