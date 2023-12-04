import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))

import walk
import file

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

def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)
    print("part 1:", sum(firstlast(list(find_digits(l))) for l in lines))
    print("part 2:", sum(firstlast(list(find_digits(l, words=True)))
                         for l in lines))
    

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)

