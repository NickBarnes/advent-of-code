import re
import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

fold_re = re.compile('^fold along ([xy])=([0-9]+)$')

lines = open(input,'r').readlines()
dots = set((int(ll[0]), int(ll[1])) for l in lines if ',' in l and (ll := l.split(',')))
folds = [(m.group(1), int(m.group(2))) for l in lines if ',' not in l and (m := fold_re.match(l))]
print(f"{len(dots)} dots, {len(folds)} folds")

def showdots(dots):
    cols = max(d[0] for d in dots)
    rows = max(d[1] for d in dots)
    a = [[' ' for _ in range(cols+1)] for _ in range(rows+1)]
    for x,y in dots:
        a[y][x] = '*'
    print('\n'.join(''.join(l) for l in a))

for i,f in enumerate(folds):
    newdots=set()
    for x,y in dots:
        if f[0] == 'x':
            newdots.add((x if x < f[1] else f[1]-(x-f[1]), y))
        else:
            newdots.add((x, y if y < f[1] else f[1]-(y-f[1])))
    dots = newdots
    if i == 0:
        print(f"after fold {i}: {len(dots)} dots")

showdots(dots)
