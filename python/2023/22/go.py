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
        self.on = set() # bricks this one rests on
        self.under = set() # bricks resting on this one

    def __repr__(self):
        return f"<{self.id}: {self.p1}-{self.p2}>"

def go(input):
    lines = parse.lines(input)
    bricks = [Brick(line, i) for i,line in enumerate(lines)]
    cols = set(col for brick in bricks for col in brick.cols)

    # Bricks all fall down in order of their minimum 'z' coordinate,
    # computing the 'on' and 'under' sets.
    base = {c:(0, None) for c in cols} # floor
    for brick in sorted(bricks, key = lambda brick: brick.z1):
        # brick falls down
        new_z1 = max(base[c][0] for c in brick.cols) + 1
        top = new_z1 + brick.z2 - brick.z1 # don't need to remember this
        for c in brick.cols:
            h, lower = base[c]
            if lower:
                if h == new_z1 - 1: # resting on lower brick
                    brick.on.add(lower)
                    lower.under.add(brick)
            base[c] = top, brick

    print("part 1, safe bricks to disintegrate:",
          sum(1 for brick in bricks
              if all(len(b.on) > 1 for b in brick.under)))

    total = 0
    for brick in bricks:
        fallen = set([brick])
        might_fall = set(b for b in brick.under)
        while might_fall:
            falling = set(b for b in might_fall if b.on <= fallen)
            if not falling: # nothing left to fall down
                break
            might_fall -= falling
            for b in falling:
                might_fall |= b.under # newly less-supported bricks
            fallen |= falling
        total += len(fallen) - 1 # don't count `brick` itself.
    print("part 2, total falling bricks:", total)
