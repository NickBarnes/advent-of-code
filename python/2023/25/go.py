def go(input):
    lines = parse.lines(input)
    edges = set()
    for line in lines:
        node, rest = line.split(':')
        others = rest.strip().split()
        for other in others:
            edges.add(frozenset((node, other)))
    edges = [tuple(edge) for edge in edges]
    components = graph.karger_stein(edges, 3)
    print("part 1, product of component sizes:",
          misc.prod(len(c) for c in components))
