import intcode

def go(input):
    ic = intcode.IntCode([int(s) for s in input.split(',')], AoC)
    if AoC.testing:
        print("part 1 (test result with no input):",
              list(ic.outputs(iter(()))))
    else:
        res = list(ic.outputs(iter([1])))
        assert len(res) == 1
        print("part 1 (BOOST keycode):", res[0])
        ic.reset()
        res = list(ic.outputs(iter([2])))
        assert len(res) == 1
        print("part 1 (distress signal coordinates):", res[0])

