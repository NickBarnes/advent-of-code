import intcode

class PrefixedIter:
    """Make an iterator which produces the values from another
    iterator preceded by a single value. The preceded iterator can be
    set after the fact by setting the `.rest` member."""

    def __init__(self, first, rest):
        self._first = first
        self._started = False
        self._stopped = False
        self.rest = rest
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._stopped:
            raise StopIteration
        if not self._started:
            self._started = True
            return self._first
        if self.rest is not None:
            res = next(self.rest, self)
            if res != self:
                return res
        self._stopped = True
        raise StopIteration

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
        iters = [PrefixedIter(phase, None) for phase in perm]
        for amp,i1,i2 in zip(amps,iters,iters[1:]):
            i2.rest = amp.outputs(inputs=i1)
        loop, thrust = itertools.tee(amps[-1].outputs(inputs=iters[-1]), 2)
        # loop the thrust back to the input, prefixed by the initial 0
        iters[0].rest = PrefixedIter(0, loop)

        best = max(list(thrust))
        if result is None or best > result:
            result = best
    print("part 2 (maximum thrust in feedback mode):", result)
