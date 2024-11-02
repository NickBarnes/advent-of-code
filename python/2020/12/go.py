line_re = re.compile('^([NSEWLRF])([0-9]+)$')

def move(x,y,c,n):
    if c == 'N':
        y += n
    elif c == 'S':
        y -= n
    elif c == 'E':
        x += n
    elif c == 'W': 
        x -= n
    return x,y
    

def run(cmds, dx, dy, way=False):
    x,y = 0,0
    for c,n in cmds:
        if c in 'NSEW':
            if way:
                dx,dy = move(dx,dy,c,n)
            else:
                x,y = move(x,y,c,n)
        elif c == 'F':
            x += dx * n
            y += dy * n
        elif c == 'L':
            assert (n // 90) * 90 == n
            while n > 0:
                dx,dy = -dy,dx
                n -= 90
        elif c == 'R':
            assert (n // 90) * 90 == n
            while n > 0:
                dx,dy = dy,-dx
                n -= 90
    return x,y

def go(input):
    cmds = [(m.group(1),int(m.group(2))) for l in parse.lines(input) if (m := line_re.match(l))]
    x,y = run(cmds, 1, 0, False)
    print(f"part 1 (using ship direction): {abs(x)+abs(y)}")
    x,y = run(cmds, 10, 1, True)
    print(f"part 2 (using waypoint): {abs(x)+abs(y)}")
