def go(input):
    lines = parse.lines(input)
    start = int(lines[0])
    buses = [(int(b), i)
             for i, b in enumerate(lines[1].split(','))
             if b != 'x']

    # part 1
    bus = sorted((b - (start % b), b) for b,_ in buses)[0]
    print("part 1 (product of bus# and wait):", bus[0]*bus[1])

    # part 2
    remainders = [(b, b-i) for b,i in buses]
    print("part 2 (timestamp of desired bus arrival pattern):",
          number.chinese_remainder(remainders)[1])
