line_re = re.compile("^([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)$")

def go(input):
    part1_passwords = 0
    part2_passwords = 0
    for l in parse.lines(input):
        m = line_re.match(l)
        lo = int(m.group(1))
        hi = int(m.group(2))
        letter = m.group(3)
        pwd = m.group(4)
        n = pwd.count(letter)
        if lo <= n <= hi:
            part1_passwords += 1
        if (pwd[lo-1] == letter or pwd[hi-1] == letter) and pwd[lo-1] != pwd[hi-1]:
            part2_passwords += 1
    print("part 1 (passwords valid with character counts):",
          part1_passwords)
    print("part 2 (passwords valid with character positions):",
          part2_passwords)
        
        
        
    
