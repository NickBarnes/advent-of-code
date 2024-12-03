insn_re = re.compile(r"mul\(([0-9]+),([0-9]+)\)|(do)\(\)|(don't)\(\)")

def compute(input, switching=False):
    sum = 0
    enabled = True
    for a,b,c,d in insn_re.findall(input):
        if c:
            enabled = True
        if d:
            enabled = False
        if a and b and (enabled or not switching):
            sum += int(a)*int(b)
    return sum

def go(input):
    print("part 1 (no switching):", compute(input))
    print("part 2 (switching):", compute(input, switching=True))
