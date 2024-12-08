def go(input):
    chars = parse.chars(input)
    locations = defaultdict(set)
    for j,row in enumerate(chars):
        for i,c in enumerate(row):
            if c != '.':
                locations[c].add((i,j))
    xlim, ylim = len(chars[0]), len(chars)
    
    antinodes = set()
    def add(x,y):
        if 0 <= x < xlim and 0 <= y < ylim:
            antinodes.add((x,y))

    def antenna_pairs():
        for antennae in locations.values():
            for x1,y1 in antennae:
                for x2,y2 in antennae:
                    if x1==x2 and y1==y2:
                        continue
                    yield x1,y1,x2,y2

    def add_line(x1,y1,x2,y2):
        dx,dy = x1-x2,y1-y2

        # "exactly in line"
        if dx and dy:
            divisor = math.gcd(dx,dy)
            dx,dy = dx/divisor,dy/divisor
        elif dx:
            dy = 1 if dy > 0 else -1
        elif dy:
            dx = 1 if dx > 0 else -1

        x,y = x2,y2
        while 0 <= x < xlim and 0 <= y < ylim:
            add(x,y)
            x,y = x+dx, y+dy
        x,y = x2,y2
        while 0 <= x < xlim and 0 <= y < ylim:
            add(x,y)
            x,y = x-dx, y-dy

    for x1,y1,x2,y2 in antenna_pairs():
        dx,dy = x1-x2,y1-y2
        add(x1+dx,y1+dy)
        add(x2-dx,y2-dy)
    print("part 1 (antinodes without resonance):", len(antinodes))

    antinodes = set()
    for x1,y1,x2,y2 in antenna_pairs():
        add_line(x1,y1,x2,y2)
    print("part 2 (antinodes with resonance):", len(antinodes))
