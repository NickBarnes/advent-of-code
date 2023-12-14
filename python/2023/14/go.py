import sys
import os
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))
import walk
import file
import interval
import misc

def load(round, rows):
    return sum(rows - j for (i,j) in round)

def roll(round, square, size, dir):
    stops = defaultdict(set)
    for i,j in square:
        if dir in 'NS':
            stops[i].add(j)
        else:
            stops[j].add(i)
    rolling = defaultdict(list)
    for i,j in round:
        if dir in 'NS':
            rolling[i].append(j)
        else:
            rolling[j].append(i)
    rolled = set()
    for i,rocks in rolling.items():
        stopped = stops[i]
        for rock in sorted(rocks, reverse=(dir in 'SE')):
            if dir in 'NW':
                j = max((s for s in stopped if s < rock), default=-1)+1
            else:
                j = min((s for s in stopped if s > rock), default=size)-1
            stopped.add(j)
            if dir in 'NS':
                rolled.add((i,j))
            else:
                rolled.add((j,i))
    return rolled

def cycle(round, square, size, count):
    pos_memo = {}
    load_memo = {}
    for i in range(count):
        for d in 'NWSE':
            round = roll(round, square, size, d)
        key = frozenset(round)
        if key in pos_memo:
            prev = pos_memo[key]
            cycle_length = i - prev
            remainder = (count - i - 1) % cycle_length
            final_pos = prev + remainder
            return load_memo[final_pos]
        pos_memo[key] = i
        load_memo[i] = load(round, size)

def go(filename):
    print(f"results from {filename}:")
    rows = file.lines(filename)
    round = [(i,j) for j,row in enumerate(rows) for i,c in enumerate(row) if c == 'O']
    square = [(i,j) for j,row in enumerate(rows) for i,c in enumerate(row) if c == '#']
    print("part 1, load after tilting north:",
          load(roll(round, square, len(rows), 'N'), len(rows)))
    print("part 2, load after a billion cycles:",
          cycle(round, square, len(rows), 1_000_000_000))

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
