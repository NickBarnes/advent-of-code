import intcode

class LazyIter:
    def __init__(self, init):
        self._queue = deque(init)
        self._stopped = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self._queue:
            self._stopped = True
        if not self._stopped:
                return self._queue.popleft()
        raise StopIteration

    def append(self, value):
        self._queue.append(value)
            
def paint(grid, ic):
    p = intgrid.V2(0,0)
    dp = intgrid.V2(0,-1)
    inputs = LazyIter([grid.get(p,0)])
    ic.reset()
    outputs = ic.outputs(inputs)
    while True:
        try:
            grid[p] = next(outputs)
            turn = next(outputs)
        except StopIteration:
             assert ic.halted
             break
        if turn == 0:
            dp = dp.ccw()
        else:
            assert turn == 1
            dp = dp.cw()
        p += dp
        inputs.append(grid.get(p,0))


def go(input):
    if AoC.testing:
        print("No test inputs for this day.")
    ic = intcode.IntCode((int(s) for s in input.split(',')), AoC)
    grid = {}
    paint(grid, ic)
    print("part 1 (panels painted from all black):", len(grid))
    grid = {intgrid.V2(0,0):1}
    paint(grid, ic)
    minx = min(p.x for p in grid)
    maxx = max(p.x for p in grid)
    miny = min(p.y for p in grid)
    maxy = max(p.y for p in grid)
    print("part 2 (code painted from single white):")
    print('\n'.join(''.join('# .'[grid.get(intgrid.V2(x,y), 2)]
                            for x in range(minx, maxx+1))
                    for y in range(miny, maxy+1)))
    
    

    
