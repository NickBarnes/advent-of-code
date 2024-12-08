def go(input):
    pairs = [l.split('-') for l in parse.lines(input)]
    caves = set(p[0] for p in pairs) | set(p[1] for p in pairs)
    rev = [(p[1],p[0]) for p in pairs]
    both = pairs + rev
    neighbours = {a:{b for a1,b in both if a == a1} for a in caves}

    caves = set(neighbours)
    smalls = set(c for c in caves if c.islower())

    assert "start" in caves
    assert "end" in caves

    def paths_to_end(cave, path, seen_smalls, twice=False):
        if cave == 'end':
            return 1
        n = 0
        for neighbour in neighbours[cave]:
            this_twice = twice
            seen = seen_smalls.get(neighbour,0)
            if seen >= 2:
                continue
            if seen == 1:
                if twice:
                    this_twice = False
                else:
                    continue
            path.append(neighbour)
            if neighbour in smalls:
                seen_smalls[neighbour] += 1
            n += paths_to_end(neighbour, path, seen_smalls, this_twice)
            path.pop()
            if neighbour in smalls:
                seen_smalls[neighbour] -= 1
        return n

    def fresh_seen():
        ss = {s:0 for s in smalls}
        ss['start'] = 99
        return ss

    p = paths_to_end("start", ["start"], fresh_seen(), twice=False)

    print(f"part 1 (paths with no more than one visit to any small cave): {p}")

    p = paths_to_end("start", ["start"], fresh_seen(), twice=True)

    print(f"part 2 (paths with a single small cave visited up to twice): {p}")
