def go(input):
    ids = parse.lines(input)
    counters = [Counter(id) for id in ids]
    twos = sum(1 for c in counters if 2 in c.values())
    threes = sum(1 for c in counters if 3 in c.values())
    print("part 1 (box ID set checksum):", twos*threes)
    
    answer = None
    for i, id1 in enumerate(ids):
        for id2 in ids[i+1:]:
            diff = None
            for j in range(len(id1)):
                if id1[j] != id2[j]:
                    if diff is not None:
                        diff = None
                        break
                    diff = j
            if diff is not None:
                answer = id1[:diff]+id1[diff+1:]
        if answer:
            break
    assert answer
    print("part 2 (letters in common of two similar IDs):", answer)


    
