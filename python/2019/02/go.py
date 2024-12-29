import intcode

def go(input):
    ic = intcode.IntCode([int(s) for s in input.split(',')], AoC)
    if not AoC.testing:
        ic.poke(1,12)
        ic.poke(2,2)

    ic.run()
    print("part 1 (code[0] after running code):",
          ic._code[0])
    if AoC.testing:
        return

    # Could certainly be more efficient
    for noun in range(100):
        for verb in range(100):
            ic.reset()
            ic.poke(1,noun)
            ic.poke(2,verb)
            ic.run()
            if ic.peek(0) == 19690720:
                print("part 2 (noun and verb to produce 19690720):",
                      100*noun + verb)
                break
        else:
            continue
        break
            
