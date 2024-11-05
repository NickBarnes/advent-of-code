def go(input):
    seats = set(int(p.replace('F','0').replace('B','1').replace('L','0').replace('R','1'),2)
                for p in parse.lines(input))
    print("part 1 (maximum seat ID):",
          max(seats))
    if len(seats) > 100:
        print("part 2 (missing seat IDs):",
              set(range(min(seats),max(seats)+1))-seats)
