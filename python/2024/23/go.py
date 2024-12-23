def go(input):
    neighbours = defaultdict(set)
    for a,b in (l.split('-') for l in parse.lines(input)):
        neighbours[a].add(b)
        neighbours[b].add(a)

    # find triangles
    triangles = set()
    for a in neighbours:
        for b in neighbours[a]:
            for c in neighbours[b] & neighbours[a]:
                triangles.add(frozenset((a,b,c)))

    ts = set(t for t in triangles if any(n.startswith('t') for n in t))
    print("part 1 (number of triangles with a 't_' node):", len(ts))

    ks = list(triangles)
    while True:
        # for each clique, look for outside nodes which are neighbour
        # to every element, and add one such node.
        newks = []
        for k in ks:
            kl = list(k)
            common = set.intersection(*((neighbours[n] - k) for n in k))
            if common:
                # only add one; could do more work to add more
                newks.append(k | {next(iter(common))})
        if not newks:
            break
        ks = list(set(newks))
    assert len(ks) == 1
    LAN_party = ks[0]
    print("part 2 (the LAN party password):",
          ','.join(sorted(LAN_party)))
