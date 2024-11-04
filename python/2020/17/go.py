def neighbours3(x,y,z):
    for dx in range(-1,2):
        for dy in range(-1,2):
            for dz in range(-1,2):
                if dx == dy == dz == 0:
                    continue
                yield x+dx,y+dy,z+dz

def neighbours4(x,y,z,w):
    for dx in range(-1,2):
        for dy in range(-1,2):
            for dz in range(-1,2):
                for dw in range(-1,2):
                    if dx == dy == dz == dw == 0:
                        continue
                    yield x+dx,y+dy,z+dz,w+dw

def generate(active, neighbours):
    for cell in set.union(*(set(neighbours(*c)) for c in active)):
        actives = sum((1 for n in neighbours(*cell)
                       if n in active))
        if cell in active:
            if 2 <= actives <= 3:
                yield cell
        else:
            if actives == 3:
                yield cell

def show3(active):
    minx = min(x for (x,y,z) in active)
    maxx = max(x for (x,y,z) in active)
    miny = min(y for (x,y,z) in active)
    maxy = max(y for (x,y,z) in active)
    minz = min(z for (x,y,z) in active)
    maxz = max(z for (x,y,z) in active)
    print('\n---\n'.join(f'z={z}\n'+
                         '\n'.join(
                             ''.join('#' if (x,y,z) in active else '.' for x in range(minx,maxx+1))
                             for y in range(miny, maxy+1))
                         for z in range(minz, maxz+1)))

def show4(active):
    minx = min(x for (x,y,z,w) in active)
    maxx = max(x for (x,y,z,w) in active)
    miny = min(y for (x,y,z,w) in active)
    maxy = max(y for (x,y,z,w) in active)
    minz = min(z for (x,y,z,w) in active)
    maxz = max(z for (x,y,z,w) in active)
    minw = min(w for (x,y,z,w) in active)
    maxw = max(w for (x,y,z,w) in active)
    print('\n---\n'.join(f'z={z},w={w}\n'+
                         '\n'.join(
                             ''.join('#' if (x,y,z,w) in active else '.' for x in range(minx,maxx+1))
                             for y in range(miny, maxy+1))
                         for z in range(minz, maxz+1)
                         for w in range(minw, maxw+1)))

def go(input):
    init = {(c,r,0)
            for r,row in enumerate(parse.chars(input))
            for c,char in enumerate(row)
            if char == '#'}

    active = init
    for i in range(6):
        active = set(generate(active, neighbours3))
    print("part 1 (active cells after 6 3D generations.", len(active))

    active = set((x,y,z,0) for (x,y,z) in init)
    for i in range(6):
        active = set(generate(active, neighbours4))
    print("part 2 (active cells after 6 4D generations.", len(active))
        
