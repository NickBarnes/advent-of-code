moves = {'^': (0,1),
         'v': (0,-1),
         '<': (-1,0),
         '>': (1,0),
         }

def deliver(instructions, santas):
    presents = Counter()
    locs = [(0,0)] * santas
    for i,c in enumerate(instructions):
        dx,dy = moves.get(c)
        x,y = locs[i % santas]
        x,y = x+dx, y+dy
        presents[(x,y)] += 1
        locs[i % santas] = x,y
    return len(presents)

def go(input):
    input = input.strip()
    if len(input) < 100: # test inputs
        print("instructions:", input)
    print("part 1 (houses visted by solo Santa):",
          deliver(input.strip(), 1))
    print("part 2 (houses visted by two Santas):",
          deliver(input.strip(), 2))
