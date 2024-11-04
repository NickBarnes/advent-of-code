tile_re = re.compile('^Tile ([0-9]+):$')

def flip(tile):
    return [''.join(r[i] for r in tile) for i in range(len(tile[0]))]

def rotate_cw(tile):
    return [''.join(r[i] for r in tile[::-1]) for i in range(len(tile[0]))]

def rotate_ccw(tile):
    return [''.join(r[-i-1] for r in tile) for i in range(len(tile[0]))]

def show(tile):
    print('\n'.join(tile))

def gridset(grid):
    return set((r,c)
               for r,row in enumerate(grid)
               for c,char in enumerate(row) if char == '#')
    

def roughness(picture):
    """Calculate 'sea roughness: how many # characters are left
    after eliminating all sea monsters."""
    monster = ['                  # ',
               '#    ##    ##    ###',
               ' #  #  #  #  #  #   ']

    picset = gridset(picture)
    rows = len(picture)
    cols = len(picture[0])

    # Does `mon` appear in `pic` at `(dr,dc)` ?
    def at(monset,dr,dc):
        return all((mr+dr,mc+dc) in picset for mr,mc in monset)

    # Rotate monster until we find some.
    def search(monster):
        for i in range(4):
            monset = gridset(monster)

            monsters = [(dr,dc)
                        for dr in range(rows)
                        for dc in range(cols)
                        if at(monset,dr,dc)]
            if (monsters):
                yield set((r+dr,c+dc) for r,c in monset for dr,dc in monsters)
            monster = rotate_cw(monster)

    monsters = list(search(monster))
    if not monsters:
        monster = flip(monster)
        monsters = list(search(monster))
    assert monsters
    assert len(monsters) == 1

    return len(picset)-len(monsters[0])

def go(input):
    tiles = {}
    edges = {}

    # update tile and edges to reflect rotation or reflection
    def update_tile(num, tile):
        tiles[num] = tile
        edges[num] = (# NESW
                      tile[0],
                      ''.join(l[-1] for l in tile),
                      tile[-1][::-1],
                      ''.join(l[0] for l in tile[::-1]))

    for t in parse.sections(input):
        tile = t[1:]
        m = tile_re.match(t[0])
        assert m
        num = int(m.group(1))
        update_tile(num, tile)

    # tiles_of_edge is central: a list of tile numbers for each edge.
    tiles_of_edge = defaultdict(list)
    for num,es in edges.items():
        for e in es:
            tiles_of_edge[e].append(num)
            # also add as reversed edge
            tiles_of_edge[e[::-1]].append(num)

    # find all tiles which have two edges not found on any other tile:
    # these must be corners
    definite_corners = set(n for n in edges
                           if sum(1 for e in edges[n]
                                  if len(tiles_of_edge[e]) == 1) == 2)

    # Remarkably in this data set, there are always exactly 4 definite
    # corners, and this gives us the answer to part 1.
    assert len(definite_corners) == 4
    print("part 1 (product of corner tile numbers):",
          misc.prod(definite_corners))

    # check each corner has a pair of adjacent unique edges
    for c in definite_corners:
        outside_edges = [i
                         for i,e in enumerate(edges[c])
                         if len(tiles_of_edge[e]) == 1]
        assert len(outside_edges) == 2
        # edges are adjacent
        assert (outside_edges[0] - outside_edges[1]) % 4 != 2

    # tiles which have a single edge not found on any other
    # tile. These must be either corners or edges. As it happens here,
    # we know that they are side tiles (as the corners are identified
    # above).
    sides_or_corners = set(n for n in edges
                           if sum(1 for e in edges[n]
                                  if len(tiles_of_edge[e]) == 1) == 1)

    # Remarkably, in this data set, there are always the right number
    # of definite edges.
    side_length = len(sides_or_corners)//4 + 2
    assert side_length * side_length == len(tiles)
    
    # Also remarkably, all edges which are not unique (and therefore
    # outside edges) are shared between exactly two tiles.
    assert max(len(ts) for ts in tiles_of_edge.values()) == 2
    
    # Therefore placement can be purely mechanical and does not need
    # to backtrack.

    # Find the unique tile which goes adjacent to tile number
    # `num` in direction `dir`. Rotate/flip the tile as necessary.
    def next_tile(num, dir):
        nonlocal tiles
        e = edges[num][dir][::-1] # find a tile which matches this
        ts = tiles_of_edge[e]
        assert num in ts
        ts.remove(num)
        assert len(ts) == 1
        next_tile = ts[0]
        if e not in edges[next_tile]:
            update_tile(next_tile, flip(tiles[next_tile]))
        assert e in edges[next_tile]

        opp = (dir + 2) % 4
        while e != edges[next_tile][opp]:
            update_tile(next_tile, rotate_cw(tiles[next_tile]))
        return next_tile

    # Make a complete row of tiles, one at a time, starting with tile
    # `t` and proceeding in direction `dir`.
    def make_row(t, dir):
        row = [t]
        for i in range(side_length-1):
            t = next_tile(t, dir)
            row.append(t)
        return row

    # arbitrarily select a corner tile and rotate it so it goes in the
    # NW corner.
    t = list(definite_corners)[0]
    while (len(tiles_of_edge[edges[t][0]]) == 2 or
           len(tiles_of_edge[edges[t][3]]) == 2):
        # top edge or left edge is shared; rotate
        update_tile(t, rotate_cw(tiles[t]))

    rows = [make_row(t, 1)] # east
    while len(rows) < side_length:
        t = next_tile(rows[-1][0], 2) # south
        rows.append(make_row(t, 1)) # east

    # check various things about this arrangement
    all_tiles = set(t for r in rows for t in r)
    assert all_tiles == set(tiles)
    assert set([rows[0][0], rows[0][-1], rows[-1][0], rows[-1][-1]]) == definite_corners
    perimeter = set.union(set(rows[0]),set(rows[-1]),set(r[0] for r in rows),set(r[-1] for r in rows))
    assert definite_corners.issubset(perimeter)
    assert sides_or_corners.issubset(perimeter)

    # Check that all tiles fit together
    for r in range(side_length-1):
        for c in range(side_length-1):
            # east edge of each tile matches west edge of tile to east.
            assert edges[rows[r][c]][1] == edges[rows[r][c+1]][3][::-1]
            # south edge of each tile matches north edge of tile to south.
            assert edges[rows[r][c]][2] == edges[rows[r+1][c]][0][::-1]
            

    # Now we can form the big picture
    def shrink_tile(tile):
        return [row[1:-1] for row in tile[1:-1]]

    def tile_row(ts):
        sts = [shrink_tile(t) for t in ts]
        return [''.join(st[i] for st in sts) for i in range(len(sts[0]))]
    
    picture = [r for row in rows for r in tile_row(tiles[t] for t in row)]
    
    print("part 2 (sea roughness after removing monsters):",
          roughness(picture))
