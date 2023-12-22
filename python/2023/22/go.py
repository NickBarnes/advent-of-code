# Observations:
# x and y coordinates are in [0,9]

brick_re = re.compile('([0-9]+),([0-9]+),([0-9]+)~([0-9]+),([0-9]+),([0-9]+)')

class Brick:
    def __init__(self, l, i):
        self.id = i
        m = brick_re.match(l)
        assert m
        x1,y1,self.z1,x2,y2,self.z2 = (int(g) for g in m.groups())
        self.p1 = (x1,y1,self.z1)
        self.p2 = (x2,y2,self.z2)
        assert self.p1 <= self.p2 # saves some code
        self.cols = set((x,y)
                        for x in range(x1,x2+1)
                        for y in range(y1,y2+1))

    def __repr__(self):
        return f"<{self.id}: {self.p1}-{self.p2}>"

def go(input):
    lines = parse.lines(input)
    bricks = [Brick(line, i) for i,line in enumerate(lines)]
    cols = set(col for brick in bricks for col in brick.cols)

    # the bricks can all fall down in order of their minimum 'z' coordinate.
    height = {c:0 for c in cols} # floor
    top_brick = {c:None for c in cols}
    for brick in sorted(bricks, key = lambda brick: brick.z1):
        # brick falls down
        brick.new_z1 = max(height[c] for c in brick.cols) + 1
        brick.on = set()
        brick.under = set()
        for c in brick.cols:
            if brick.new_z1 > 1: # some lower brick
                if height[c] == brick.new_z1 - 1: # a lower brick here
                    supporter = top_brick[c]
                    brick.on.add(supporter)
                    supporter.under.add(brick)
            height[c] = brick.new_z1 + brick.z2 - brick.z1
            top_brick[c] = brick
    print("part 1, safe bricks to disintegrate:",
          sum(1 for brick in bricks
              if all(len(b.on) > 1 for b in brick.under)))

    total = 0
    for brick in bricks:
        gone = set([brick])
        might_go = set(b for b in brick.under)
        while might_go:
            going = set(b for b in might_go if b.on.issubset(gone))
            if not going: # nothing left to fall down
                break
            might_go -= going
            for g in going:
                might_go |= g.under # newly less-supported bricks
            gone |= going
        total += len(gone) - 1 # don't count `brick` itself.
    print("part 2, total falling bricks:", total)
