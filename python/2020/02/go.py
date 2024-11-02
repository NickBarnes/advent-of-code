# Template for AoC daily solution. To add to imports, see
# util/__init__.py.

line_re = re.compile("^([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)$")

def go(input):
    part1 = []
    part2 = []
    for l in parse.lines(input):
        m = line_re.match(l)
        lo = int(m.group(1))
        hi = int(m.group(2))
        letter = m.group(3)
        pwd = m.group(4)
        n = pwd.count(letter)
        if lo <= n <= hi:
            part1.append(pwd)
        if (pwd[lo-1] == letter or pwd[hi-1] == letter) and pwd[lo-1] != pwd[hi-1]:
            part2.append(pwd)
    print(f"part 1: {len(part1)}")
    print(f"part 2: {len(part2)}")
        
        
        
    
