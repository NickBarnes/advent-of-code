def nth(start, N):
    """Find the Nth number said in the game, given the starting numbers."""
    seen = {}
    for i,n in enumerate(start[:-1]):
        seen[n] = i
    last = start[-1]
    i = len(start)
    while i < N:
        k = i - seen[last] - 1 if last in seen else 0
        seen[last] = i-1
        last = k
        i += 1
    return last
    

def go(input):
    start = [int(x) for x in input.split(',')]
    print("part 1 (2020th number):", nth(start, 2020))
    print("part 2 (thirty millionth number):", nth(start, 30000000))
