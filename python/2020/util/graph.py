import heapq
import random
import math

def shortest_tree(start, weights):
    """Find the shortest paths in a weighted network from `start` to
    all other nodes. `weights` is a function node -> [(node,
    weight)]. Dijkstra's algorithm.

    """
    grey = [(0, start)]
    shortest = {start: 0}

    while grey:
        d, p = heapq.heappop(grey)
        if shortest[p] < d: # already seen at shorter distance
            continue
        for n,w in weights(p):
            if n not in shortest or shortest[n] > d + w:
                heapq.heappush(grey, (d + w, n))
                shortest[n] = d + w
    return shortest

def shortest_path(start, end, weights, heuristic):
    """Find the shortest path in a weighted network from `start` to
    `end`. `weights` is a function node -> [(node, weight)].
    `heuristic` is a function node -> estimated distance to end.
    Returns the total path length and a list of the nodes on the
    path.  Take care of the constraints on `heuristic` (including:
    `heuristic(end)` must be zero). A-star algorithm.

    """
    grey = [(heuristic(start), start)]
    shortest = {start: 0}
    cameFrom = {}

    def reconstruct():
        path = []
        node = end
        while node in cameFrom:
            path.append(node)
            node = cameFrom[node]
        return list(reversed(path))

    while grey:
        score, node = heapq.heappop(grey)
        if node == end:
            return shortest[node], reconstruct()
        for next,weight in weights(node):
            dist = shortest[node] + weight
            if next not in shortest or shortest[next] > dist:
                cameFrom[next] = node
                shortest[next] = dist
                heapq.heappush(grey, (dist + heuristic(next), next))

def grid(xmax, ymax, diagonal=False):
    """Return a neighbour function for a 2D grid size `xmax` by `ymax`. If
    `diagonal` then include diagonal neighbours.

    """
    def neighbours(p):
        x,y = p
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (not diagonal) and dx and dy:
                    continue
                newx = x+dx
                newy = y+dy
                if newx >= 0 and newx < xmax and newy >= 0 and newy < ymax:
                    yield newx, newy
    return neighbours

def karger(edges, size):
    """Find a cut of the graph defined by `edges` (a list of pairs of
    nodes) into two components separated by at most `size`
    edges. Karger's Contraction Algorithm (slow).

    """
    min_cut = len(edges)
    while min_cut > size:
        graph = edges[:]
        nodes = set(n for edge in graph for n in edge)
        component = {n:n for n in nodes}
        members = {n:set([n]) for n in nodes}
        while len(nodes) > 2:
            a,b = random.choice(graph)
            # remove b
            nodes.remove(b)
            members[a] |= members[b]
            for n in members[b]:
                component[n] = a
            del members[b]
            graph = [(component[a],component[b])
                     for a,b in graph if component[a] != component[b]]
        cut = len(graph)
        if cut < min_cut:
            min_cut = cut
            components = list(members.values())
    return components

def karger_stein(edges, size):
    """Find a cut of `graph` into two components separated by at most
    `size` edges. Karger-Stein algorithm, which in theory should be quicker
    than Karger (above) but in practice seems about the same.

    """
    def contract(members, edges, size):
        # contract until we have `size` nodes remaining.
        # members: node -> set of original nodes
        # edges: [(a,b), where a != b and a,b are in members]
        # returns members, edges.
        component = {node:node for node in members}
        merged = {node: set([node]) for node in members}
        while len(merged) > size:
            a,b = random.choice(edges)
            # remove b
            merged[a] |= merged[b]
            for node in merged[b]:
                component[node] = a
            del merged[b]
            edges = [(component[a],component[b])
                     for a,b in edges if component[a] != component[b]]
        # construct supernode sets
        # We started with some supernodes (the 'members' argument)
        # and have merged some of them.
        return ({s: set(mem for k in l for mem in members[k])
                 for s, l in merged.items()},
                edges)

    def recursive(members, edges):
        # members: node -> set of original nodes
        # edges: [(a,b), where a != b and a,b are in members]
        # returns a cut length and a list of sets of component members.
        n = len(members)
        if n <= 6:
            supernodes, edges = contract(members, edges, 2)
            return len(edges), list(supernodes.values())
        target = math.floor(1 + n / math.sqrt(2))
        supernodes, edges = contract(members, edges, target)
        cut1, components1 = recursive(supernodes, edges)
        cut2, components2 = recursive(supernodes, edges)
        if cut1 < cut2:
            return cut1, components1
        else:
            return cut2, components2
    
    min_cut = len(edges)
    nodes = set(n for e in edges for n in e)
    min_components = None
    while min_cut > size:
        members = {n:set([n]) for n in nodes}
        cut, components = recursive(members, edges)
        if cut < min_cut:
            min_cut = cut
            min_components = components
    return min_components

