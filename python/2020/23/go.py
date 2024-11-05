def rotate(s,i):
    i = i % len(s)
    return s[i:]+s[:i]

# Part 1 is easy enough we can just do it with strings
def part1(cups):
    N = len(cups)
    current = cups[0]
    for i in range(100):
        current_pos = cups.index(current)
        cups = rotate(cups, current_pos+1)
        out = cups[:3]
        cups = cups[3:]
        left = set(cups)
        target = chr(ord(current) - 1)
        while target not in left:
            if target > min(left):
                target = chr(ord(target)-1)
            else:
                target = max(left)
        pos = cups.index(target)
        cups = cups[:pos+1]+out+cups[pos+1:]
        current = cups[(cups.index(current) + 1) % len(cups)]
    return rotate(cups, cups.index('1'))[1:]

# Part 2 is much larger and needs linked lists
cupmap = {}

class Cup:
    def __init__(self, label):
        self.label = label
        cupmap[label] = self

def part2(cups):
    # make circular list of cups
    cuplist = [Cup(int(c)) for c in cups]
    for i, cup in enumerate(cuplist[:-1]):
        cup.next = cuplist[i+1]
    topcup = int(max(cups))
    lastcup = cuplist[-1]
    while(topcup) < 1_000_000:
        topcup += 1
        lastcup.next = Cup(topcup)
        lastcup = lastcup.next
    lastcup.next = cuplist[0] # close the circle

    currentcup = cupmap[int(cups[0])]
    for i in range(10_000_000):
        outcup = currentcup.next
        outlabels = {outcup.label, outcup.next.label, outcup.next.next.label}
        target = (currentcup.label - 2) % 1_000_000 + 1
        while target in outlabels:
            target = (target - 2) % 1_000_000 + 1
        targetcup = cupmap[target]

        currentcup.next = outcup.next.next.next # remove
        outcup.next.next.next = targetcup.next # insert
        targetcup.next = outcup # insert

        currentcup = currentcup.next # move right

    return cupmap[1].next.label * cupmap[1].next.next.label

def go(input):
    cups = input.strip()
    print("part 1 (only a few cups):",
          part1(cups))

    print("part 2 (loads of cups):",
          part2(cups))
    
