dirs = {'U': (0,-1), # Y grows down
        'D': (0,1),
        'L': (-1,0),
        'R': (1,0),
        }

pad1 = [
'123',
'456',
'789'
]

pad2 = [
'  1  ',
' 234 ',
'56789',
' ABC ',
'  D  ']

def find(pad,x,y,instrs):
    for c in instrs:
        dx,dy = dirs[c]
        if 0 <= y+dy < len(pad) and 0 <= x+dx < len(pad[y+dy]) and pad[y+dy][x+dx] != ' ':
                x,y = x+dx,y+dy
    return x,y,pad[y][x]

def go(input):
    lines = parse.lines(input)

    # part 1
    x,y = 1,1
    code = ''
    for l in lines:
        x,y,c = find(pad1,x,y,l)
        code += c
    print("part 1 (code with conventional key-pad):", code)

    # part 2
    x,y = 0,2
    code = ''
    for l in lines:
        x,y,c = find(pad2,x,y,l)
        code += c
    print("part 2 (code with novel key-pad):", code)


