# what's the load of a given set of round rocks?
def load(round, rows):
    return sum(rows - j for (i,j) in round)

# given positions of rolling and stopped rocks on a row of length
# 'size', find the positions of the rolling rocks after tilting the
# row in direction `dir' (True or False).
memo = {}
def roll_row(rocks, stops, size, dir):
    key = (tuple(rocks), tuple(stops), size, dir)
    if key in memo:
        return memo[key]
    res = set()
    for rock in sorted(rocks, reverse=dir):
        if dir:
            j = min((s for s in stops if s > rock), default=size)-1
        else:
            j = max((s for s in stops if s < rock), default=-1)+1
        stops.add(j)
        res.add(j)
    memo[key] = res
    return res

# Given grid positions of round and square rocks, on a square grid of
# given size, find the grid positions of the round rocks after tilting
# the grid in direction 'dir' (N, S, E, W).
def roll(round, square, size, dir):
    stops = defaultdict(set)
    for i,j in square:
        if dir in 'NS':
            stops[i].add(j)
        else:
            stops[j].add(i)
    rolling = defaultdict(set)
    for i,j in round:
        if dir in 'NS':
            rolling[i].add(j)
        else:
            rolling[j].add(i)
    rolled = set()
    for i,rocks in rolling.items():
        for j in roll_row(rocks, stops[i], size, dir in 'SE'):
            if dir in 'NS':
                rolled.add((i,j))
            else:
                rolled.add((j,i))
    return rolled

# return load after `count` rinse cycles.
def cycle(round, square, size, count):
    pos_memo = {}
    load_memo = {}
    for i in range(count):
        for d in 'NWSE':
            round = roll(round, square, size, d)
        key = frozenset(round)
        if key in pos_memo:
            prev = pos_memo[key]
            loop = i - prev
            remainder = (count - i - 1) % loop
            final_pos = prev + remainder
            return load_memo[final_pos]
        pos_memo[key] = i
        load_memo[i] = load(round, size)

def go(input):
    rows = parse.lines(input)
    round = [(i,j) for j,row in enumerate(rows) for i,c in enumerate(row) if c == 'O']
    square = [(i,j) for j,row in enumerate(rows) for i,c in enumerate(row) if c == '#']
    print("part 1, load after tilting north:",
          load(roll(round, square, len(rows), 'N'), len(rows)))
    print("part 2, load after a billion cycles:",
          cycle(round, square, len(rows), 1_000_000_000))
