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
    def __init__(self,c, jokers = False):
        self.c = c
        if jokers:
            self.rank = 'J23456789TQKA'.index(c)
        else:
            self.rank = '23456789TJQKA'.index(c)

    def __eq__(self, other):
        return self.c == other.c

    def __gt__(self, other):
        return self.rank > other.rank

    def __repr__(self):
        return f"Card({self.c})"

cards = {c:Card(c) for c in 'AKQJT98765432'}
jw_cards = {c:Card(c, jokers=True) for c in 'AKQJT98765432'}

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
        # fundamental hand type is the size of the maximum set
        self.hand_type = max(c.values(), default=0) + self.jokers
        # two exceptions, which we can represent with intermediate values
        if self.hand_type == 3 and len(c) == 2:
            self.hand_type = 3.5 # full house
        elif self.hand_type == 2 and len(c) == 3:
            self.hand_type = 2.5 # two pair

    def __eq__(self, other):
        return self.hand == other.hand

    def __gt__(self, other):
        return (self.hand_type > other.hand_type
                or (self.hand_type == other.hand_type and
                    self.cards > other.cards)) # uses Card ordering
    
    def __repr__(self):
        return f"<{self.hand}, {self.hand_type}({self.jokers})>"

def find_ranks(hands, jokers = False):
    # pair all hands with their initial indices, and sort by hand
    ranked = sorted((Hand(h, jokers), i) for i,h in enumerate(hands))
    # enumerate the ranking, sort by initial index and yield the ranks
    for i,k in sorted((i,k) for k, (_, i) in enumerate(ranked)):
        yield k+1

def go(filename):
    print(f"results from {filename}:")
    lines = file.words(filename)
    ranks = find_ranks(h for (h,_) in lines)
    print("part 1: ", sum(int(bid) * rank
                          for (_, bid),rank in zip(lines,ranks)))
    jw_ranks = find_ranks((h for (h,_) in lines), jokers = True)
    print("part 2: ", sum(int(bid) * rank
                          for (_, bid),rank in zip(lines,jw_ranks)))

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
