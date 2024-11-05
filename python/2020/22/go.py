from collections import deque

# Game from part 1. Could use an array of players, but with only two
# it's not worth it.

def combat(deck1, deck2):
    player1 = deque(deck1)
    player2 = deque(deck2)
    round = 1
    while player1 and player2:
        c1,c2 = player1.popleft(),player2.popleft()
        if c1 > c2:
            player1.append(c1)
            player1.append(c2)
        else:
            player2.append(c2)
            player2.append(c1)
    if player1:
        return 1, player1
    else:
        return 2, player2

# Game from part 2. Really simple.

def recursive_combat(deck1, deck2, depth=1):
    memory = set()
    player1 = deque(deck1)
    player2 = deque(deck2)
    round = 1
    while player1 and player2:
        k = tuple(player1),tuple(player2)
        if k in memory:
            return 1, player1
        memory.add(k)
        c1,c2 = player1.popleft(),player2.popleft()
        if c1 <= len(player1) and c2 <= len(player2):
            # recurse!
            round_winner, _ = recursive_combat(list(player1)[:c1],
                                               list(player2)[:c2],
                                               depth+1)
        else:
            round_winner = 1 if c1 > c2 else 2
        if round_winner == 1:
            player1.append(c1)
            player1.append(c2)
        else:
            player2.append(c2)
            player2.append(c1)
    if player1:
        return 1, player1
    else:
        return 2, player2

# How to score a winning deck.
def score(deck):
    return sum(i*k for i,k in enumerate(reversed(list(deck)),start=1))

def go(input):
    sections = parse.sections(input)
    assert sections[0][0] == 'Player 1:'
    assert sections[1][0] == 'Player 2:'
    player1 = [int(l) for l in sections[0][1:]]
    player2 = [int(l) for l in sections[1][1:]]
    id, winner = combat(player1, player2)
    print(score(winner))

    id, winner = recursive_combat(player1, player2)
    print(score(winner))
