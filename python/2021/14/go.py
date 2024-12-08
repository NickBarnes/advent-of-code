import re
import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

lines = open(input,'r').readlines()

template = lines[0].strip()

rule_re = re.compile('([A-Z][A-Z]) -> ([A-Z])$')
rules = {m.group(1):m.group(2) for l in lines if (m := rule_re.match(l))}
pair_rules = {k:(k[0]+v,v+k[1]) for k,v in rules.items()}

print(f"{template}, {len(rules)} rules")

from collections import Counter

def apply(pairs):
    newpairs = Counter()
    for p,n in pairs.items():
        for newpair in pair_rules.get(p,[p]):
            newpairs[newpair] += n
    return newpairs

def final_frequencies(template, rounds):
    pairs = Counter(template[i:i+2] for i in range(len(template)-1))

    for i in range(rounds):
        pairs = apply(pairs)

    counts = Counter()
    for p,n in pairs.items():
        counts[p[0]] += n
        counts[p[1]] += n
    # The above should count every character twice except for the first and last

    counts[template[0]] += 1
    counts[template[-1]] += 1

    s = [(v/2,k) for k,v in counts.items()]
    s.sort()
    return s

s = final_frequencies(template, 10)

print(f"After 10 rounds: Most frequent '{s[-1][1]}' ({s[-1][0]}. Least frequent '{s[0][1]}' ({s[0][0]}). Difference (answer 1): {s[-1][0]-s[0][0]}.")

s = final_frequencies(template, 40)

print(f"After 40 rounds: Most frequent '{s[-1][1]}' ({s[-1][0]}. Least frequent '{s[0][1]}' ({s[0][0]}). Difference (answer 2): {s[-1][0]-s[0][0]}.")
