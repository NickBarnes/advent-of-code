# Template for AoC daily solution. To add to imports, see
# util/__init__.py.

def go(input):
    lines = parse.lines(input)
    d = {int(i) for i in lines}
    for i in d:
        if 2020-i in d:
            print("part 1: %d" % (i * (2020-i)))
            break
    
    d2 = {i+j: (i,j) for i in d for j in d}
    for k in d:
        if 2020-k in d2:
            print("part 2: %d" % (k * d2[2020-k][0] * d2[2020-k][1]))
            break


