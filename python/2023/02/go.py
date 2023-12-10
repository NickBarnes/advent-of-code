import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))
import walk
import file
import misc
import re

col_re = re.compile(' *([0-9]+) (red|blue|green)')

class Game:
    def __init__(self, s):
        assert s.startswith('Game ')
        id, desc = s.split(':')
        self.id = int(id[5:])
        self.rounds = [{m.group(2):int(m.group(1))
                        for c in r.split(',')
                        if (m := col_re.match(c))}
                       for r in desc.split(';')]
    
    def possible(self, cols):
        return all(r.get(k,0) <= n
                   for r in self.rounds
                   for k,n in cols.items())

    def power(self):
        return misc.prod(max(r.get(col,0) for r in self.rounds)
                         for col in ['red','green','blue'])

def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)
    games = [Game(l) for l in lines]
    print("part 1, sum of possible games:",
          sum([g.id for g in games
               if g.possible({"red":12, "green":13, "blue":14})]))
    print("part 2, sum of powers of all gamess:",
          sum(g.power() for g in games))

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
