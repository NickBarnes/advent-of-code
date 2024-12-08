# items in rucksacks.

# each item is a letter with a value defined like this:
def val(c):
    if 'a' <= c <= 'z': return ord(c)-ord('a')+1
    return ord(c)-ord('A')+27

def go(input):
    sacks = parse.lines(input)

    # Each sack has an even number of items, and one item in both
    # the first and second half. Total of the values of the duplicates:
    total = sum(val((set(s[:len(s)//2]) & set(s[len(s)//2:])).pop())
                for s in sacks)
    print(f"part 1 (sum of odd items): {total}")

    # Each group of three sacks has one item in all three sacks (the
    # 'badge'). Total of the values of the badges.

    # There's some itertools trick to get groups-of-N but
    # I can't remember it off-hand.
    badge_total = sum(val((set(group[0]) & set(group[1]) & set(group[2])).pop())
                      for group in [sacks[i:i+3]
                                    for i in range(0, len(sacks), 3)])
    print(f"part 2 (total badge priority): {badge_total}")
