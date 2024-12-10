def go(input):
    gifts = [sorted(int(dim) for dim in l.split('x'))
             for l in parse.lines(input)]
    print("part 1 (total wrapping paper):",
          sum(3*a*b + 2*a*c + 2*b*c for a,b,c in gifts))
    print("part 2 (total ribbon):",
          sum(2*(a+b) + a*b*c for a,b,c in gifts))
