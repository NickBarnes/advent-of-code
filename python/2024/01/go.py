def go(input):
    l1, l2 = zip(*parse.words(input))
    l1 = sorted(map(int,l1))
    l2 = sorted(map(int,l2))
    d = sum(abs(loc1-loc2) for loc1,loc2 in zip(l1,l2))
    print(f"part 1 (total distance): {d}")

    c = Counter(l2)
    t = sum(loc * c[loc] for loc in l1)
    print(f"part 2 (similarity score): {t}")

    
    
