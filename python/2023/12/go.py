@functools.cache
def ways(pattern, counts):
    if not pattern: # end of the pattern
        return 0 if counts else 1 # succeed if we're at the end of the search
    elif not counts: # not looking for any more
        return 0 if '#' in pattern else 1 # succeed if there's nothing left
    else:
        c = pattern[0]
        if c == '.': # ignore leading '.'
            return ways(pattern[1:], counts)

        else:
            # possible spring: how many ways if it is a spring?
            if len(pattern) < counts[0] or '.' in set(pattern[:counts[0]]):
                with_spring = 0 # group of yeses or maybes too small
            elif len(pattern) > counts[0] and pattern[counts[0]] == '#':
                with_spring = 0 # too many!
            else: # group just right!
                with_spring = ways(pattern[counts[0]+1:], counts[1:])

            if c == '?': # possible spring: count both ways
                return with_spring + ways(pattern[1:], counts)
            else: # actual spring
                return with_spring

def unfold(pattern, counts):
    return '?'.join([pattern] * 5), counts * 5

def go(input):
    lines = parse.lines(input)
    rows = [(l[0], tuple(int(x) for x in l[1].split(',')))
            for line in lines if (l := line.split())]
    print("part 1, total arrangements:",
          sum(ways(*row) for row in rows))
    print("part 2, total arrangements with unfolding:",
          sum(ways(*unfold(*row)) for row in rows))
