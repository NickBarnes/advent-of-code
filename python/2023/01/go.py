def find_digits(s, words=False):
    for i in range(len(s)):
        if s[i].isdigit():
            yield s[i]
        elif words:
            for n,d in enumerate(['one', 'two', 'three', 'four', 'five',
                                  'six', 'seven', 'eight', 'nine']):
                if s[i:].startswith(d):
                    yield str(n+1)

def firstlast(d):
    return int(d[0]+d[-1]) if d else 0

def go(input):
    lines = parse.lines(input)
    print("part 1, sum:", sum(firstlast(list(find_digits(l)))
                                for l in lines))
    print("part 2, sum:", sum(firstlast(list(find_digits(l, words=True)))
                                for l in lines))
