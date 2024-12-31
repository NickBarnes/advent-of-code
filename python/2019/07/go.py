import intcode

def go(input):
    code = [int(c) for c in input.split(',')]

    # part 1
    ic = intcode.IntCode(code, AoC)
    result = 0
    for perm in itertools.permutations(range(5)):
        signal = 0
        for phase in perm:
            ic.reset()
            signal = next(ic.outputs(inputs=iter([phase, signal])))
        if signal > result:
            result = signal
    print("part 1 (maximum thrust in non-feedback mode)", result)
            
    # part 2
    # We will use a set of amps
    amps = [intcode.IntCode(code, AoC) for _ in range(5)]
    result = None
    for perm in itertools.permutations(range(5,10)):
        for amp in amps:
            amp.reset()
        # for this permutation, build iterators to connect the amps
        iters = [intcode.PrefixInputs(phase, None) for phase in perm]
        for amp,i1,i2 in zip(amps,iters,iters[1:]):
            i2.rest = amp.outputs(inputs=i1)
        loop, thrust = itertools.tee(amps[-1].outputs(inputs=iters[-1]), 2)
        # loop the thrust back to the input, prefixed by the initial 0
        iters[0].rest = intcode.PrefixInputs(0, loop)

        best = max(list(thrust))
        if result is None or best > result:
            result = best
    print("part 2 (maximum thrust in feedback mode):", result)
