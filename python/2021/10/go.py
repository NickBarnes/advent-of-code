def go(input):
    nav = parse.lines(input)

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

    corrupted = sum(s for l in nav if (s := score(l)) > 0)
    print(f"part 1 (corrupted score): {corrupted}")

    incomplete_scores = sorted([-s for l in nav if (s := score(l.strip())) < 0])
    middle_score = incomplete_scores[len(incomplete_scores)//2]
    print(f"part 2 (middle incompleted score): {middle_score}")
