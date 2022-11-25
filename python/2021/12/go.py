import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]
print(input)

pairs = [l.strip().split('-') for l in open(input,'r').readlines()]
caves = set(p[0] for p in pairs) | set(p[1] for p in pairs)
rev = [(p[1],p[0]) for p in pairs]
both = pairs + rev
neighbours = {a:{b for a1,b in both if a == a1} for a in caves}

caves = set(neighbours)
smalls = set(c for c in caves if c.islower())

assert "start" in caves
assert "end" in caves

print(f"{len(caves)} caves")
print(f"{len(pairs)} tunnels")

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

print(f"paths to end with no more than one visit to any small cave (answer 1) {p}")

p = paths_to_end("start", ["start"], fresh_seen(), twice=True)

print(f"paths to end with a single small cave visited up to twice (answer 2) {p}")
