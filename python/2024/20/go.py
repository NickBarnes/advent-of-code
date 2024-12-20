def go(input):
    grid = intgrid.IntGrid(parse.lines(input))
    start = grid.find_only('S')
    end = grid.find_only('E')

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

    # Find all the cheats (defined as (start,end) pairs
    def find_cheats(grid, margin, path, distances, total, max_cheat_len):
        cheats = defaultdict(set)
        max_len = total - margin
        for i in range(len(path)):
            p = path[i]
            for x in range(max(0, p.x - max_cheat_len), min(grid.width, p.x + max_cheat_len + 1)):
                y_range = max_cheat_len - abs(p.x-x)
                for y in range(max(0, p.y - y_range), min(grid.height, p.y + y_range + 1)):
                    # we can cheat to x,y
                    n = intgrid.V2(x,y)
                    cheat_len = abs(p.x - x) + abs(p.y - y)
                    if distances.get(n, grid.area) < distances[p]: # further down the track
                        total_len = i + cheat_len + distances[n]
                        if total_len <= max_len:
                            cheats[total_len].add((p, n))
        return cheats

    distances, path = legit_path(grid)
    if (AoC.verbose):
        print ('\n'.join(''.join(('#' if grid.get(p) == '#'
                                  else str(distances[p] % 10) if p in distances else '.')
                                 for i in range(grid.width)
                                 if (p := intgrid.V2(i,j)))
                         for j in range(grid.height)))
        
    total = len(path)-1 # fence-post
    margin = 1 if AoC.testing else 100
    cheats = find_cheats(grid, margin, path, distances, total, 2)
    if AoC.verbose:
        for k in sorted(cheats, reverse=True):
            print(f"{len(cheats[k])} cheats saving {total-k}")
    print(f"part 1 (cheats length up to 2, saving at least {margin}):",
          sum(len(l) for l in cheats.values()))

    margin = 50 if AoC.testing else 100
    cheats = find_cheats(grid, margin, path, distances, total, 20)
    if AoC.verbose:
        for k in sorted(cheats, reverse=True):
            print(f"{len(cheats[k])} cheats saving {total-k}")
    print(f"part 2 (cheats length up to 20, saving at least {margin}):",
          sum(len(l) for l in cheats.values()))
