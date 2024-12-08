slopes = {'>':(1,0),
          '<':(-1,0),
          '^':(0,-1),
          'v':(0,1)}
dirs = list(slopes.values())

def neighbours(grid, seen, node, icy = True):
    i,j = node
    if icy and grid[node] in slopes:
        try_dirs = [slopes[grid[node]]]
    else:
        try_dirs = dirs
    return [n for di,dj in try_dirs
            if (n := (i+di,j+dj))
            if n in grid and n not in seen]

# Find all paths from the current node through the grid to any node
# which is either the end or a junction. Returns a list [(dest, dist)]
# where dist is the length of the path.
def paths(grid, end, node, icy = True):
    paths = []
    seen = set([node])
    for n in neighbours(grid, seen, node, icy): # let's look this way
        d = 1
        while n != end:
            seen.add(n)
            nx = list(neighbours(grid, seen, n, icy))
            if not nx: # nowhere to go
                n = None
                break
            if len(nx) > 1: # junction
                break
            n = nx[0]
            d += 1
        if n: # we had somewhere to go
            paths.append((n, d))
    return paths

# Build a graph node -> [(next, distance)]
def graph(grid, start, end, icy):
    graph = {}
    grey = set([start])
    seen = set([start])
    while grey:
        n = grey.pop()
        seen.add(n)
        ps = paths(grid, end, n, icy)
        graph[n] = ps
        for n,_ in ps:
            if n not in seen:
                grey.add(n)
                seen.add(n)
    return graph

def longest_from(graph, node, end, seen):
    if node == end:
        return 0
    seen += node
    ls = [d + best
          for nx,d in graph[node]
          if not (nx & seen)
          and (best := longest_from(graph, nx, end, seen)) >= 0]
    seen -= node
    return max(ls, default=-1)

def longest(grid, start, end, icy):
    g = graph(grid, start, end, icy)
    # represent each node with a bit, and node sets with bit masks. 2x faster.
    bit = {n: 1<<i for i,n in enumerate(g)}
    g2 = {bit[n1]: [(bit[n2],w) for n2,w in l] for n1,l in g.items()}
    return longest_from(g2, bit[start], bit[end], 0)

def go(input):
    lines = parse.lines(input)
    rows = len(lines)
    grid = {(i,j):c
            for j,line in enumerate(lines)
            for i,c in enumerate(line) if c != '#'}
    starts = [i for i,j in grid if j == 0]
    assert len(starts) == 1
    start = (starts[0],0)
    ends = [i for i,j in grid if j == rows-1]
    assert len(ends) == 1
    end = (ends[0],rows-1)

    print("part 1, longest path when icy:", longest(grid,start,end,icy=True))
    print("part 2, longest path when not icy:", longest(grid,start,end,icy=False))
