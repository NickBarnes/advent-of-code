import random

# Hmm, Karger's algorithm
def karger(orig_graph, target):
    min_cut = len(orig_graph)
    while min_cut > target:
        graph = orig_graph[:]
        elims = {}
        while True:
            nodes = set(n for edge in graph for n in edge)
            if len(nodes) == 2:
                break
            a,b = random.choice(graph)
            # remove b
            elims[a] = elims.get(a,0) + elims.get(b,0) + 1
            new_graph = []
            for edge in graph:
                if b not in edge:
                    new_graph.append(edge)
                elif b == edge[0] and a != edge[1]:
                    new_graph.append((a, edge[1]))
                elif b == edge[1] and a != edge[0]:
                    new_graph.append((edge[0], a))
            graph = new_graph
        cut = len(graph)
        if cut < min_cut:
            min_cut = cut
            min_elims = {n: elims.get(n,0)+1 for n in nodes}
    return min_elims

def go(input):
    lines = parse.lines(input)
    graph = set()
    for line in lines:
        node, rest = line.split(':')
        others = rest.strip().split()
        for other in others:
            graph.add(frozenset((node, other)))
    graph = [tuple(edge) for edge in graph]
    components = karger(graph, 3)
    print("part 1, product of component sizes:",
          misc.prod(components.values()))
