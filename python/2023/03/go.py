import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

import re
digits = re.compile('[0-9]+')

def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)
    partsum = 0
    stars = {}
    for j, l in enumerate(lines):
        for m in digits.finditer(l):
            n = int(m.group(0))
            found_symbol = False
            def check(x,y):
                nonlocal found_symbol
                if x < 0 or x >= len(l) or y < 0 or y >= len(lines):
                    return
                c = lines[y][x]
                if c == '.' or c.isdigit():
                    return
                found_symbol = True
                if c == '*':
                    stars[(x,y)] = stars.get((x,y),[]) + [n]
            for dy in (-1,1):
                for x in range(m.start()-1,m.end()+1):
                    check(x, j+dy)
            check(m.start()-1, j)
            check(m.end(), j)
            if found_symbol:
                partsum += n
    print(f"part one: sum of unattached parts: {partsum}")

    gears = []
    for p,nums in stars.items():
        if len(nums) == 2:
            gears.append(nums)
    gearsum = sum(a*b for (a,b) in gears)
    print(f"part two: sum of gears: {gearsum}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
