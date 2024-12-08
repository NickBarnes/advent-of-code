# Elf cleaning ranges

# Does the first range wholly contain the second?
def contain(r1,r2):
    return r2[0] >= r1[0] and r2[1] <= r1[1]

# Do the two ranges overlap at all?
def overlap(r1,r2):
    return r1[0] <= r2[1] and r2[0] <= r1[1]

def go(input):
    ranges = [l.split(',') for l in parse.lines(input)]
    values = [[(int(s[0]),int(s[1])) for r in l if (s := r.split('-'))] for l in ranges]

    c1 = sum(1 for v in values if contain(*v) or contain(*reversed(v)))
    print(f"part 1 (pairs wholly overlap): {c1}")

    c2 = sum(1 for v in values if overlap(*v))
    print(f"part 2 (pairs partly overlap): {c2}")
