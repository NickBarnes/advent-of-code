part_re = re.compile(r'([0-9]+) ([A-Z]+)')

def ore(recipes, order, fuel):
    required = Counter({'FUEL':fuel})
    ore = 0
    for item in order:
        count = required[item]
        n, recipe = recipes[item]
        times = (count + n - 1)//n
        for m, ingr in recipe:
            required[ingr] += times * m
    return required['ORE']
    

def go(input):
    recipes = {'ORE': (1,[])}
    for line in parse.lines(input):
        parts = [(int(x),y) for x,y in part_re.findall(line)]
        assert len(parts) > 1
        res = parts[-1]
        assert res[1] not in recipes
        recipes[res[1]] = (res[0], parts[:-1])

    # topo sort
    order = [] # will be total order FUEL, ..., ORE
    used_for = defaultdict(set)
    for res, (_, l) in recipes.items():
        for _,ingr in l:
            used_for[ingr].add(res)
    grey = {'FUEL'}
    while grey:
        ingr = grey.pop()
        order.append(ingr)
        _, l = recipes[ingr]
        for _,needed in l:
            used_for[needed].remove(ingr)
            if not used_for[needed]:
                grey.add(needed)
    print("part 1 (ORE required for 1 FUEL):", ore(recipes, order, 1))

    high = 1
    while ore(recipes, order, high) < 1_000_000_000_000:
        high *= 2
    low = high // 2

    while low < high-1:
        mid = (low + high) // 2
        if ore(recipes, order, mid) < 1_000_000_000_000:
            low = mid
        else:
            high = mid
    print("part 2 (FUEL produced by a trillion ORE):", low)

        
        
        
        
            
        
        
