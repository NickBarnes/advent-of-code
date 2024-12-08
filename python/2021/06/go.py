import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

ages = [int(s) for s in open(input,'r').read().split(',')]
print(f"{len(ages)} lanternfish")
agemap = {i:sum(1 for a in ages if a==i) for i in range(8)}

def days(map,n):
    for _ in range(n):
        new = {i-1:map[i] for i in map.keys() if i > 0 and map[i] != 0}
        new[8] = map.get(0,0)
        new[6]=new.get(6,0)+map.get(0,0)
        map = new
    return map

after80 = sum(days(agemap, 80).values())
after256 = sum(days(agemap, 256).values())

print(f"answer 1 {after80}, answer 2 {after256}")

