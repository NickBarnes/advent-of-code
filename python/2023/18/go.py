line_re = re.compile('([UDLR]) ([0-9]+) \(#([0-9a-f]{6})\)')

dirs = {'L':(-1,0),
        'R':(1,0),
        'U':(0,-1),
        'D':(0,1)}

decode = {i:c for i,c in enumerate('RDLU')}

def lagoon(instructions):
    points = defaultdict(set)
    x,y = 0,0
    for (dx,dy),d,_ in instructions:
        points[x].add(y)
        x,y = x + dx * d, y + dy * d
    assert x == 0 and y == 0 # trench returns to origin

    cols = sorted((x, list(sorted(y))) for x,y in points.items())
    ranges = interval.Intervals([])
    x = cols[0][0]
    total = 0
    for (xn,ys) in cols:
        rows = set(y for i in ranges.ints for y in (i.base, i.limit))
        total += (xn - x) * (len(ranges) + ranges.count())
        # look at each trench along this column
        for y1, y2 in zip(ys[::2], ys[1::2]):
            newi = interval.Intervals([(y1,y2)])
            if newi & ranges: # removes part of existing ranges
                ranges -= newi
                # we have to adjust for squares in this column
                total += len(newi)
                if y1 in rows and y2 in rows:
                    total += 1
                elif y1 not in rows and y2 not in rows:
                    total -= 1
            else: # this trench adds to existing ranges
                ranges |= newi
        x = xn
    assert len(ranges) == 0
    return total

def go(input):
    instructions = [(dirs[m.group(1)], int(m.group(2)), int(m.group(3),base=16))
                    for l in parse.lines(input) if (m := line_re.match(l))]
    print("part 1, small lagoon area:", lagoon(instructions))
    instructions = [(dirs[decode[x % 16]], x // 16, None) for _,_,x in instructions]
    print("part 2, large lagoon area:", lagoon(instructions))
        
