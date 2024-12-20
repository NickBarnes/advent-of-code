def go(input):
    grid = intgrid.IntGrid(parse.lines(input))
    start = grid.find_only('S')
    end = grid.find_only('E')


    # Return a distance dictionary p -> distance-to-end and a path
    # dictionary steps-from-start -> p, for the unique legitimate path
    # through the grid from the start to the end.

    def legit_path(grid):
        p = end
        d = 0
        distance = {p: d}
        while p != start:
            d += 1
            ns = set()
            for dp in intgrid.ortho_dirs.values():
                n = p+dp
                if grid.get(n) != '#' and n not in distance:
                    ns.add(n)
            assert len(ns) == 1
            p = ns.pop()
            distance[p] = d
        total = d
        return distance, {total-d:n for n,d in distance.items()}

    # Find all the cheats, defined as (start,end) pairs, no more than
    # `max_cheat_len` Manhattan distance apart, which save at least
    # `margin` steps compared to the legit path `path` (length
    # `total`) using the distance array `distances`.

    def find_cheats(grid, margin, path, distances, total, max_cheat_len):
        cheats = defaultdict(set)
        max_len = total - margin
        for i in range(len(path)):
            p = path[i]
            for dx in range(-max_cheat_len, max_cheat_len + 1):
                x = p.x + dx
                if x < 0 or x >= grid.width: continue
                y_range = max_cheat_len - abs(dx)
                for dy in range(-y_range, y_range + 1):
                    y = p.y + dy
                    if y < 0 or y >= grid.height: continue
                    # we can cheat to x,y
                    n = intgrid.V2(x,y)
                    total_len = i + abs(dx) + abs(dy) + distances.get(n, grid.area)
                    if total_len <= max_len:
                        cheats[total_len].add((p, n))
        return cheats

    distances, path = legit_path(grid)
    total = len(path)-1 # fence-post

    if (AoC.verbose):
        print ('\n'.join(''.join(('.' if grid.get(p) == '#' else
                                  str(distances[p] % 10) if p in distances else ' ')
                                 for i in range(grid.width)
                                 if (p := intgrid.V2(i,j)))
                         for j in range(grid.height)))
        
    # part 1
    margin = 1 if AoC.testing else 100
    cheats = find_cheats(grid, margin, path, distances, total, 2)
    if AoC.verbose:
        for k in sorted(cheats, reverse=True):
            print(f"{len(cheats[k])} cheats saving {total-k}")
    print(f"part 1 (cheats length up to 2, saving at least {margin}):",
          sum(len(l) for l in cheats.values()))

    # part 2
    margin = 50 if AoC.testing else 100
    cheats = find_cheats(grid, margin, path, distances, total, 20)
    if AoC.verbose:
        for k in sorted(cheats, reverse=True):
            print(f"{len(cheats[k])} cheats saving {total-k}")
    print(f"part 2 (cheats length up to 20, saving at least {margin}):",
          sum(len(l) for l in cheats.values()))
