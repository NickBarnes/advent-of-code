import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

segments=set('abcdefg')
inputs = [l.strip().split('|') for l in open(input,'r').readlines()]
uniques = [s[0].split() for s in inputs]
outputs = [s[1].split() for s in inputs]
ones = sum(sum(1 for i in o if len(i) == 2) for o in outputs)
sevens = sum(sum(1 for i in o if len(i) == 3) for o in outputs)
fours = sum(sum(1 for i in o if len(i) == 4) for o in outputs)
eights = sum(sum(1 for i in o if len(i) == 7) for o in outputs)
total = ones+sevens+fours+eights

print(f"{ones} ones, {sevens} sevens, {fours} fours, {eights} eights, answer 1 {total}")

total = 0
def setstr(s): return ''.join(sorted(s))

for i in range(len(inputs)):
    counts = {l: sum(1 for x in uniques[i] if l in x) for l in segments}
    b = set([k for k,v in counts.items() if v == 6][0])
    e = set([k for k,v in counts.items() if v == 4][0])
    f = set([k for k,v in counts.items() if v == 9][0])
    one = set([u for u in uniques[i] if len(u) == 2][0])
    seven = set([u for u in uniques[i] if len(u) == 3][0])
    four = set([u for u in uniques[i] if len(u) == 4][0])
    c = one - f
    a = seven - one
    d = four - c - f - b
    g = segments - a - b - c - d - e - f
    digits = {setstr(one): 1,
              setstr(a | c | d | e | g): 2,
              setstr(a | c | d | f | g): 3,
              setstr(four): 4,
              setstr(a | b | d | f | g): 5,
              setstr(segments - c): 6,
              setstr(seven): 7,
              setstr(segments): 8,
              setstr(segments - e):9,
              setstr(segments - d): 0}
    output = 0
    for o in outputs[i]:
        output = output * 10 + digits[setstr(set(o))]
    total += output
print(total)
