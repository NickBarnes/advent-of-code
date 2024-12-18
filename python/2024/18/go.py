def go(input):
    bytes = [intgrid.V2(*(int(v) for v in l.split(',')))
             for l in parse.lines(input)]
    testing = len(bytes) < 100
    width,height = (7,7) if testing else (71,71)
    start = intgrid.V2(0,0)
    end = intgrid.V2(width-1,height-1)
             
    prefix = 12 if testing else 1024

    def path_after_bytes(n):
        # Return the shortest path after `n` bytes have fallen.
        # Result is (path length, nodes (excluding start)).
        corrupted = set(bytes[:n])

        # A-star
        def weights(p):
            for dp in intgrid.ortho_dirs.values():
                np = p+dp
                if np.in_box(width, height) and np not in corrupted:
                    yield np,1

        def heuristic(p): return (width-p.x) + (height-p.y)

        return graph.shortest_path(start, end, weights, heuristic)

    print("part 1 (shortest path after some bytes fall):",
          path_after_bytes(prefix)[0])
    
    base, limit = prefix, len(bytes)
    last_path = []
    while limit > base+1:
        trial = (base + limit) // 2
        res = path_after_bytes(trial)
        if res:
            last_path = res[1]
            base = trial
        else:
            limit = trial
    print("part 2 (first byte which blocks path):", bytes[base])

    # Display resulting grid.
    grid = {}
    for p in bytes[:base]:
        grid[(p.x,p.y)] = '#'
    for p in last_path:
        grid[(p.x,p.y)] = 'O'
    grid[(start.x,start.y)] = 'O'

    print('\n'.join(''.join(grid.get((i,j),'.') for i in range(width))
                    for j in range(height)))
