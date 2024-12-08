def go(input):
    lines = parse.lines(input)

    digits = '=-012'

    val = {}
    inv = {}
    for i,d in enumerate(digits):
        val[d] = i-2
        inv[i-2] = d

    def from_snafu(s):
        return val[s[-1]] + (from_snafu(s[:-1]) * 5 if len(s) > 1 else 0)

    def to_snafu(n):
        return (to_snafu((n+2) // 5) if n > 2 else "") + inv[((n+2) % 5) - 2]

    print(f"part 1 (sum of fuel requirements): {to_snafu(sum(from_snafu(l) for l in lines))}")
