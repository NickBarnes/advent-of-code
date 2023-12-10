import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))
import walk
import file

class Card:
    def __init__(self, s):
        id, data = s.split(':')
        self.id = int(id[5:])
        winning, given = data.split('|')
        winning = set(int(w) for w in winning.split())
        given = set(int(g) for g in given.split())
        self.matches = len(winning & given)
        self.count = 1

    def points(self):
        return 0 if self.matches == 0 else (1 << self.matches-1)

def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)
    cards = {c.id: c for l in lines if (c := Card(l))}
    point_total = sum(c.points() for c in cards.values())
    print(f"part 1, points: {point_total}")

    # Do part 2 mechanically because that's more than fast enough
    for n in range(1,len(cards)+1):
        c = cards[n]
        for i in range(c.matches):
            cards[n+i+1].count += c.count
    card_count = sum(c.count for c in cards.values())
    print(f"part 2, cards: {card_count}")
        

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
