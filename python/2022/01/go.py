def go(input):
    elves = parse.sections(input)
    calories = sorted([sum(int(l) for l in e) for e in elves])
    print(f"part 1 (max calories of any elf): {calories[-1]}")
    print(f"part 2 (total calories of top three elves): {sum(calories[-3:])}")
