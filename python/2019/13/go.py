import intcode

def play(ic, active = True):
    screen = {}
    tiles = " #O-o"
    score = None
    inputs = intcode.LazyInputs([])
    outs = ic.outputs(inputs)
    started = False
    my_turn = False
    ballx, paddlex = None,None
    while True:
        try:
            x, y, tile = next(outs), next(outs), next(outs)
            if x == -1 and y == 0:
                score = tile
                if AoC.verbose:
                    print("score:", score)
                started = active
            else:
                c = tiles[tile]
                if c == '-':
                    if paddlex is None:
                        paddley = y
                    else:
                        assert y == paddley
                    paddlex = x
                elif c == 'o':
                    ballx, bally = x,y
                    # move after ball moves
                    my_turn = True
                if AoC.verbose:
                    if screen.get((x,y),'.') == 'O':
                        assert tiles[tile] == ' '
                        print(f"Clearing block at {x},{y}")
                screen[(x,y)] = tiles[tile]
                    
        except StopIteration:
            break
        if started and my_turn and ballx is not None and paddlex is not None:
            if ballx > paddlex: # move right
                inputs.append(1)
            elif ballx < paddlex: # move left
                inputs.append(-1)
            else: # hold
                inputs.append(0)
            my_turn = False
    return screen, score

def show(screen, score):
    minx = min(x for x,_ in screen)
    maxx = max(x for x,_ in screen)
    miny = min(y for _,y in screen)
    maxy = max(y for _,y in screen)
    print('\n'.join(''.join(screen.get((x,y),'.')
                            for x in range(minx,maxx+1))
                    for y in range(miny, maxy+1)))
    if score is not None:
        print("score:", score)

def go(input):
    ic = intcode.IntCode((int(s) for s in input.split(',')), AoC)
    screen, score = play(ic, active=False)
    print("part 1 (number of blocks):",
          Counter(screen.values())['O'])
    if AoC.verbose:
        show(screen, score)

    ic.reset()
    ic.poke(0,2) # play for free
    inputs = intcode.LazyInputs([0,0,0,-1,-1,-1])
    screen, score = play(ic)
    print("part 2 (score when all blocks cleared):", score)
    if AoC.verbose:
        show(screen, score)
