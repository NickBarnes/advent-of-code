import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))
import walk
import file
import interval
import misc

# memoizer for `ways`
mem = {}
def ways(pattern, counts):
    # memoized
    key = (pattern,tuple(counts))
    if key in mem:
        return mem[key]

    if not pattern: # end of the pattern
        if not counts: # end of the search
            res = 1
        else: # still looking, so we've failed
            res = 0
    elif not counts: # not looking for any more
        if '#' in pattern: # but there is one, so we've failed
            res = 0
        else: # none left, so we can set all the ? to . and succeed
            res = 1
    else:
        c = pattern[0]
        if c == '.': # ignore leading '.'
            res = ways(pattern[1:], counts)

        else:
            # possible spring: how many ways if it is a spring?
            if len(pattern) < counts[0] or '.' in set(pattern[:counts[0]]):
                with_spring = 0 # group of yeses or maybes too small
            elif len(pattern) > counts[0] and pattern[counts[0]] == '#':
                with_spring = 0 # too many!
            else: # group just right!
                with_spring = ways(pattern[counts[0]+1:], counts[1:])

            if c == '?': # possible spring: count both ways
                res = with_spring + ways(pattern[1:], counts)
            else: # actual spring
                res = with_spring
    # memoize
    mem[key] = res
    return res

def unfold(pattern, counts):
    return '?'.join([pattern] * 5), counts * 5

def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)
    rows = [(l[0], [int(x) for x in l[1].split(',')])
            for line in lines if (l := line.split())]
    print("part 1, total arrangements:",
          sum(ways(*row) for row in rows))
    print("part 2, total arrangements with unfolding:",
          sum(ways(*unfold(*row)) for row in rows))

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
