def go(input):
    course = [(s[0], int(s[1])) for l in parse.lines(input) if (s := l.split())]
    tf = sum(n for (d,n) in course if d == 'forward')
    td = sum(n for (d,n) in course if d == 'down')
    tu = sum(n for (d,n) in course if d == 'up')
    depth = td-tu
    product = tf * depth
    print(f"part 1 (product of depth and forward motion): {product}")

    h = 0
    aim = 0
    d = 0
    for (direction, distance) in course:
        if direction == 'down':
            aim += distance
        elif direction == 'up':
            aim -= distance
        elif direction == 'forward':
            h += distance
            d += distance * aim
    product = h * d
    print(f"part 2 (with corrected aim): {product}")

        

