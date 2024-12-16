def go(input):
    chars = parse.chars(input)
    locations = defaultdict(set)
    for j,row in enumerate(chars):
        for i,c in enumerate(row):
            if c != '.':
                locations[c].add(intgrid.V2(i,j))
    xlim, ylim = len(chars[0]), len(chars)
    
    antinodes = set()
    def add(p):
        if 0 <= p.x < xlim and 0 <= p.y < ylim:
            antinodes.add(p)

    def antenna_pairs():
        for antennae in locations.values():
            for a1 in antennae:
                for a2 in antennae:
                    if a1 == a2:
                        continue
                    yield a1,a2

    def add_line(a1,a2):
        dp = a1-a2

        # "exactly in line"
        if not dp.ortho():
            divisor = math.gcd(dp.x,dp.y)
            dp //= divisor
        elif dp.x:
            dp = intgrid.V2(1 if dx > 0 else -1,0)
        elif dp.y:
            dp = intgrid.V2(0, 1 if dy > 0 else -1)

        p = a2
        while 0 <= p.x < xlim and 0 <= p.y < ylim:
            add(p)
            p += dp
        p = a2
        while 0 <= p.x < xlim and 0 <= p.y < ylim:
            add(p)
            p -= dp

    for a1,a2 in antenna_pairs():
        dp = a1-a2
        add(a1+dp)
        add(a2-dp)
    print("part 1 (antinodes without resonance):", len(antinodes))

    antinodes = set()
    for a1,a2 in antenna_pairs():
        add_line(a1,a2)
    print("part 2 (antinodes with resonance):", len(antinodes))
