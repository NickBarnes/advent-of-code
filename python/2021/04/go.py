class Board:
    def __init__(self, lines, n):
        self._boardno = n
        self._won = False
        self._rows = [[int(x) for x in l.split()] for l in lines]
        self._nrows = len(self._rows)
        self._ncols = len(self._rows[0])
        for j in range(self._nrows):
            assert len(self._rows[j]) == self._ncols
        self._numbers = {c:(i,j)
                         for j in range(self._nrows)
                         for i in range(self._ncols)
                         if (c := self._rows[j][i]) is not None}
        self._unmarked = sum(c for r in self._rows for c in r)
        self._rowsleft = {j:self._ncols for j in range(self._nrows)}
        self._colsleft = {i:self._nrows for i in range(self._ncols)}

    def call(self, n):
        if not self._won:
            i,j = self._numbers.get(n, (None, None))
            if i is not None:
                self._unmarked -= n
                self._rowsleft[j] -= 1
                self._colsleft[i] -= 1
                if self._rowsleft[j] == 0 or self._colsleft[i] == 0:
                    self._won = True
                    return self._unmarked * n
    
def go(input):
    boards = parse.sections(input)
    assert len(boards[0]) == 1
    calls = [int(s) for s in boards[0][0].split(',')]
    boards = [Board(b, i) for i,b in enumerate(boards[1:])]
    
    def play():
        lastwon = None
        for i,c in enumerate(calls):
            for bn,b in enumerate(boards):
                if (r := b.call(c)) is not None:
                    if lastwon is None:
                        print(f"part 1 (final score of first winning board): {r}")
                    lastwon = (i, c, bn, r)
        i,c,bn,r = lastwon
        print(f"part 2 (final score of last winning board): {r}")
    
    play()

