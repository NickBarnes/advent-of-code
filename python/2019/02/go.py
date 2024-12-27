import intcode

def go(input):
    orig = [int(s) for s in input.split(',')]
    code = orig.copy()
    if not AoC.testing:
        code[1] = 12
        code[2] = 2
    intcode.run(code)
    print("part 1 (code[0] after running code):",
          code[0])
    if AoC.testing:
        return

    # Could certainly be more efficient
    for noun in range(100):
        for verb in range(100):
            code = orig.copy()
            code[1] = noun
            code[2] = verb
            intcode.run(code)
            if code[0] == 19690720:
                print("part 2 (noun and verb to produce 19690720):",
                      100*noun + verb)
                break
        else:
            continue
        break
            
