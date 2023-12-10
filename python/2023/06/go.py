import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))
import walk
import file
import math
import misc

def winners(t,d):
    first_winner = math.floor(t/2 - math.sqrt(t*t/4 -d) + 1)
    last_winner = math.ceil(t/2 + math.sqrt(t*t/4 -d) - 1)
    return last_winner - first_winner + 1

def winner_prod(td):
    return misc.prod(winners(int(t),int(d)) for t,d in td)

def go(filename):
    print(f"results from {filename}:")
    words = file.words(filename)
    assert len(words) == 2
    assert words[0][0] == 'Time:'
    assert words[1][0] == 'Distance:'
    td = list(zip(words[0][1:], words[1][1:]))
    print(f"part 1, multiple races: {winner_prod(td)}")
    td = [(''.join(words[0][1:]), ''.join(words[1][1:]))]
    print(f"part 2, single race: {winner_prod(td)}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
