def go(input):
    chars = parse.chars(input)
    rows = len(chars)
    cols = len(chars[0])
    
    round = 0
    moving = True
    while moving:
        moving = False
        moves = []
        for r in range(rows):
            for c in range(cols):
               if chars[r][c] == '>' and chars[r][(c + 1) % cols] == '.':
                   moves.append((r,c))
        for r,c in moves:
               moving = True
               chars[r][c] = '.'
               chars[r][(c+1) % cols] = '>'
        moves = []
        for r in range(rows):
            for c in range(cols):
               if chars[r][c] == 'v' and chars[(r + 1) % rows][c] == '.':
                   moves.append((r,c))
        for r,c in moves:
               moving = True
               chars[r][c] = '.'
               chars[(r+1) % rows][c] = 'v'
        round += 1
    print("part 1 (round when the sea cucumbers don't move):", round)
