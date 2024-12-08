def go(input):
    diagnostics = [int(l, base=2) for l in parse.lines(input)]
    m = max(diagnostics)
    n = len(diagnostics)

    # part 1
    h = n/2
    bit = 1
    gamma = 0
    epsilon = 0
    while (bit < m):
        k = sum(1 for d in diagnostics if (d & bit == bit))
        if k+k > n:
            gamma += bit
        else:
            epsilon += bit
        bit *= 2
    product = gamma * epsilon
    print(f"part 1 (power consumption): {product}")

    # part 2
    import math
    topbit = 1 << int(math.log(m,2))

    def find(dl, keep_common):
        bit = topbit
        while len(dl) > 1 and bit > 0:
            k = sum(1 for d in dl if (d & bit == bit))
            if k + k >= len(dl):
                common_bit = bit
            else:
                common_bit = 0
            keep_bit = common_bit if keep_common else bit - common_bit
            dl = list(d for d in dl if d & bit == keep_bit)
            bit = int(bit/2)
        return dl[0]

    bit = topbit
    common = find(diagnostics, True)
    rare = find(diagnostics, False)
    product = common * rare
    print(f"part 2 (life support rating): {product}")


