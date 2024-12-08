def go(input):
    counter = Counter(input)
    print("part 1 (Santa's final floor):", counter['('] - counter[')'])

    pos = 0
    for i, c in enumerate(input, start=1):
        if c == '(':
            pos += 1
        elif c == ')':
            pos -= 1
        if pos == -1:
            print("part 2 (first basement instruction):", i)
            break
