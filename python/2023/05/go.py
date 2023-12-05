import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))

import walk
import file

# I brute-forced part 2 in C (see part2.c) and then wrote a much more
# pleasant version with interval arithmetic.

from interval import *

class Map:
    def __init__(self, lines):
        desc = lines[0]
        d1,d2 = desc.split()
        assert(d2 == 'map:')
        self.source,t,self.dest = d1.split('-')
        assert(t == 'to')
        ranges = [[int(x) for x in l.split()] for l in lines[1:]]
        # convert to intervals
        self.ranges = [(Interval(s_start, s_start + length),
                        d_start-s_start)
                       for (d_start, s_start, length) in ranges]

    def apply(self, v):
        for (s_int, delta) in self.ranges:
            if v in s_int:
                return v + delta
        return v

    # ooh look at the shiny shiny
    def apply_intervals(self, inter):
        hits = []
        ints = inter.ints
        for (s, delta) in self.ranges:
            misses = []
            for i in ints:
                hit = i & s
                if hit: hits.append(hit.offset(delta))
                misses += list(i - s)
            ints = misses
        return Intervals([(x.base, x.limit) for l in (hits, ints) for x in l])

# Seed numbers for part 1
def part1seeds(s):
    assert(len(s) == 1)
    seeds = s[0].split()
    assert(seeds[0] == 'seeds:')
    return [int(x) for x in seeds[1:]]

# Seed intervals for part 2
def part2seeds(s):
    assert(len(s) == 1)
    seed_pairs = s[0].split()
    assert(seed_pairs[0] == 'seeds:')
    intervals = []
    for i in range(len(seed_pairs)//2):
        base = int(seed_pairs[i*2+1])
        length = int(seed_pairs[i*2+2])
        intervals.append((base, base+length))
    # combine and normalise
    return Intervals(intervals)

def min_location(seeds, maps):
    min_loc = None
    min_seed = None
    for s in seeds:
        v = s
        for map in maps:
            v = map.apply(v)
        if min_loc is None or v < min_loc:
            min_loc = v
            min_seed = s
    return min_loc

def min_location_inters(inters, maps):
    for m in maps:
        inters = m.apply_intervals(inters)
    return inters.ints[0].base

def go(filename):
    print(f"results from {filename}:")
    sections = file.sections(filename)
    maps = [Map(s) for s in sections[1:]]
    print("Part 1: minimum location "
          f"{min_location(part1seeds(sections[0]), maps)}")
    print("Part 2: minimum location "
          f"{min_location_inters(part2seeds(sections[0]),maps)}")
    
        
if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
