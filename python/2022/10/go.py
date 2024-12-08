def go(input):
    words = parse.words(input)
    cycle = 0
    x = 1
    # total signal strength
    signal = 0
    # pixel grid
    grid = [['?' for _ in range(40)] for _ in range(6)]

    def tick():
        nonlocal cycle, signal, grid
        row = cycle // 40
        col = cycle % 40
        cycle += 1 # this is now the true cycle number (AoC counters start from 1)
        if col == 19: # offset by one (AoC counters start from 1)
            signal += x * cycle
        grid[row][col]= '#' if abs(x-col) < 2 else ' '

    for line in words:
        if line[0] == "noop":
            tick()
        elif line[0] == 'addx':
            tick()
            tick()
            x += int(line[1])

    print(f"part 1 (total signal strength): {signal}")
    print("part 2 (CRT display):")
    print('\n'.join(''.join(row) for row in grid))
