import sys

input='bingo.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

f = open(input,'r')

calls = [int(s) for s in f.readline().strip().split(',')]
print(f"{len(calls)} calls")

lines = f.readlines()

def board_end(lines):
    for i in range(len(lines)):
        if not lines[i].strip():
            return i
    return len(lines)

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

boards = []
while lines:
    e = board_end(lines)
    if e > 0:
        boards.append(Board(lines[0:e], len(boards)))
    lines = lines[e+1:]
print(f"{len(boards)} boards")

def play():
    lastwon = None
    for i,c in enumerate(calls):
        for bn,b in enumerate(boards):
            if (r := b.call(c)) is not None:
                if lastwon is None:
                    print(f"first win call {i}:{c} board {bn} answer 1 {r}")
                lastwon = (i, c, bn, r)
    i,c,bn,r = lastwon
    print(f"last win call {i}:{c} board {bn} answer 2 {r}")

play()

