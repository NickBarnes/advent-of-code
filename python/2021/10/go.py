import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

nav = open(input,'r').readlines()

pairs=['[]','{}','()','<>']

match = {p[0]:p[1] for p in pairs}

mismatch_score = {')': 3,
                  ']': 57,
                  '}': 1197,
                  '>': 25137,
}

complete_score = {')': 1,
                  ']': 2,
                  '}': 3,
                  '>': 4,
}

def score(l):
    stack = []
    for i, c in enumerate(l):
        if c in match:
            stack.append(match[c])
        elif c != stack.pop():
            return mismatch_score[c]
    total = 0
    for c in stack[::-1]:
        total = total * 5 + complete_score[c]
    return -total

corrupted = sum(s for l in nav if (s := score(l.strip())) > 0)
print(f"corrupted score (answer 1) {corrupted}")

incomplete_scores = sorted([-s for l in nav if (s := score(l.strip())) < 0])
middle_score = incomplete_scores[len(incomplete_scores)//2]
print(f"incompleted score (answer 2) {middle_score}")

    

            
                
