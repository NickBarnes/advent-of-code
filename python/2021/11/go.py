def go(input):
    octo = [[int(c) for c in l] for l in parse.lines(input)]
    original = [l[:] for l in octo]
    rows = len(octo)
    cols = len(octo[0])

    neighbourhood = [(i,j) for i in range(-1,2) for j in range(-1,2) if i or j]

    flashed = set()

    def bump(r,c):
        if not (0 <= r < rows and 0 <= c < cols):
            return 0
        octo[r][c] += 1
        if octo[r][c] > 9 and (r,c) not in flashed:
            flashed.add((r,c))
            return 1 + sum(bump(r+i,c+j) for i,j in neighbourhood)
        return 0

    def tick():
        nonlocal flashed
        flashed = set()
        flashes = sum(bump(r,c) for r in range(rows) for c in range(cols))
        for r,c in flashed:
            octo[r][c] = 0
        return len(flashed)

    flashes100 = sum(tick() for i in range(100))
    print(f"part 1 (flashes in first 100 steps): {flashes100}")

    octo = original

    t = 1
    while True:
        n = tick()
        if n == rows * cols:
            break
        t = t + 1
    print(f"part 2 (first simultaneous flash time): {t}")
