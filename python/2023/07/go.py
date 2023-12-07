import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))
import walk
import file
import functools
from collections import Counter

@functools.total_ordering
class Card:
    def __init__(self, c, i):
        self.c = c
        self.rank = i

    def __eq__(self, other):
        return self.c == other.c

    def __gt__(self, other):
        return self.rank > other.rank

    def __repr__(self):
        return f"Card({self.c})"

cards = {c:Card(c,i) for i,c in enumerate('23456789TJQKA')}
jw_cards = {c:Card(c, i) for i,c in enumerate('J23456789TQKA')}

@functools.total_ordering
class Hand:
    def __init__(self, hand, jokers):
        self.hand = hand
        self.cards = [(jw_cards if jokers else cards)[c] for c in hand]
        c = Counter(hand)
        if jokers:
            self.jokers = c['J']
            del c['J']
        else:
            self.jokers = 0
        # fundamental hand type ('kind') is the size of the maximum set
        self.kind = max(c.values(), default=0) + self.jokers
        # two exceptions, which we can represent with intermediate values
        if self.kind == 3 and len(c) == 2: # only two card types
            self.kind = 3.5 # full house
        elif self.kind == 2 and len(c) == 3: # only three card types
            self.kind = 2.5 # two pair

    def __eq__(self, other):
        return self.hand == other.hand

    def __gt__(self, other):
        return ((self.kind, self.cards) >
                (other.kind, other.cards)) # uses Card ordering
    
    def __repr__(self):
        return f"<{self.hand}, {self.kind}({self.jokers})>"

def winnings(lines, jokers = False):
    # pair all hands with their initial indices, and sort by hand
    ranked = sorted((Hand(h, jokers), i, int(b))
                    for i, (h, b) in enumerate(lines))
    # enumerate the ranking, multiply rank by the bid
    return sum((k+1) * b for k, (_, i ,b) in enumerate(ranked))

def go(filename):
    print(f"results from {filename}:")
    lines = file.words(filename)
    print("part 1: ", winnings(lines))
    print("part 2: ", winnings(lines, jokers = True))

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
