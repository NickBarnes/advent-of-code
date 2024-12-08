import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

crabs = [int(s) for s in open(input,'r').read().split(',')]
crabs.sort()
if len(crabs) % 2 == 1:
    median = crabs[len(crabs) // 2]
    fuel = sum(abs(c-median) for c in crabs)
else:
    m1 = crabs[len(crabs) // 2 - 1]
    m2 = crabs[len(crabs) // 2]
    f1 = sum(abs(c-m1) for c in crabs)
    f2 = sum(abs(c-m2) for c in crabs)
    if f1 > f2:
        fuel = f2
        median = m2
    else:
        fuel = f1
        median = m1

print(f"{len(crabs)} crabs median {median} fuel {fuel}")

maxpos = max(crabs)
bestfuel = None
bestpos = None
for i in range(maxpos):
    fuel = sum(n*(n+1)/2 for c in crabs if (n := abs(c-i)))
    if bestfuel is None or fuel < bestfuel:
        bestfuel = fuel
        bestpos = i

print(f"best {bestpos} fuel {bestfuel}")
