# Comms handset

# Find first position with N unique consecutive characters.

def go(input):
    for l in parse.lines(input):
        if not l: continue
        print("part 1 (4 unique):",
              next(i for i in range(4, len(l)) if len(set(l[i-4:i])) == 4))
        print("part 2 (14 unique):",
              next(i for i in range(14, len(l)) if len(set(l[i-14:i])) == 14))
