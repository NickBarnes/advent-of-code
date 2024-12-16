import functools

@functools.total_ordering # So that V2(x,y) sorts as (x,y)
class V2: # Hmm, could use a namedtuple?
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return V2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return V2(self.x - other.x, self.y - other.y)

    def __floordiv__(self, other):
        return V2(self.x // other, self.y // other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other): # useful for sorting. Sorts as (x,y).
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def __hash__(self):
        return hash((self.x,self.y))

    def cw(self):
        return V2(-self.y, self.x)

    def ccw(self):
        return V2(self.y, -self.x)

    def ortho(self):
        return self.x == 0 or self.y == 0

    def __str__(self):
        return f"{self.x},{self.y}"

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.x},{self.y}>"

all_dirs = {'^': V2(0,-1),
            '7': V2(1,-1),
            '>': V2(1,0),
            'J': V2(1,1),
            'v': V2(0,1),
            'L': V2(-1,1),
            '<': V2(-1,0),
            'r': V2(-1,-1),
            }

ortho_dirs = {c:v for c,v in all_dirs.items() if c in '^v<>'}

class IntGrid:
    def __init__(self, lines, ignore='.'):
        self._grid = {V2(i,j): c
                      for j,l in enumerate(lines)
                      for i,c in enumerate(l)
                      if c != ignore}
        self._ignore = ignore
        self.height = len(lines)
        self.width = len(lines[0])
        self.area = self.height * self.width

    def __iter__(self):
        return iter(self._grid)

    def items(self):
        return self._grid.items()

    def find(self, char):
        return (p for p,c in self._grid.items() if c == char)

    def find_only(self, char):
        candidates = list(self.find(char))
        assert len(candidates) == 1
        return candidates[0]

    def get(self, p):
        return self._grid.get(p)

    def set(self, p, char):
        self._grid[p] = char

    def set_all(self, ps, char):
        for p in ps:
            self._grid[p] = char

    def move(self, p1, p2):
        assert p2 not in self._grid
        self._grid[p2] = self._grid[p1]
        del self._grid[p1]

    def move_all(self, ps, dp):
        moved = {p+dp:self._grid[p] for p in ps}
        for p in ps:
            assert p in self._grid
            del self._grid[p]
        self._grid.update(moved)

    # Find the orthogonally-connected set of grid cells
    # which have the same value as p.

    def ortho_region(self, p):
        grey = {p}
        region = {p}
        seen = {p}

        id = self._grid[p]
        while grey:
            p = grey.pop()
            for dp in ortho_dirs.values():
                n = p + dp
                if n not in seen:
                    seen.add(n)
                    if self._grid.get(n) == id:
                        grey.add(n)
                        region.add(n)
        return region

    # Find all the orthogonally-connected single-value regions of a grid.

    def all_regions(self):
        white = set(self._grid)
        regions = []
        while white:
            p = white.pop()
            found = self.ortho_region(p)
            regions.append((self._grid[p], found))
            white = white - found
        return regions

    def show(self):
        return('\n'.join(''.join(self._grid.get(V2(i,j),' ')
                                 for i in range(self.width))
                         for j in range(self.height)))

    def __repr__(self):
        return f"<{self.__class__.__name__}: {len(self._grid)} cells in {self.width}x{self.height}>"
