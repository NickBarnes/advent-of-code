line_re = re.compile(r'^([a-z ]+)( \(contains ([a-z ,]+)\))$')

def go(input):
    foods = []
    warns = defaultdict(list)
    appears = Counter()
    ingredients = set()
    for l in parse.lines(input):
        m = line_re.match(l)
        assert m
        ingreds = set(m.group(1).split())
        appears.update(ingreds)
            
        allergs = set(m.group(3).split(', ')) if m.group(2) else set()
        foods.append((ingreds, allergs))
        for a in allergs:
            warns[a].append(ingreds)
        ingredients.update(ingreds)
    # for any given allergen, the ingredient that contains it must be
    # in the ingredients list for every food that warns of it.
    suspects = {a: set.intersection(*warns[a])
                for a in warns.keys()}
    # So this is the set of all suspect ingredients
    all_suspects = set.union(*suspects.values())

    # And this is the set of all non-suspect ingredients.
    frees = ingredients - all_suspects
    print("part 1 (total appearances of definitely-free ingredients):",
          sum(appears[i] for i in frees))

    toxic = []
    # Any ingredient which is only suspect for one allergen must be
    # the ingredient containing that allergen, so can't contain any
    # other ("Each ingredient contains zero or one allergen."). Record
    # that and remove it from the suspect lists for other
    # allergens. Repeat.
    while suspects:
        new_toxins = {a: list(il)[0] for a,il in suspects.items() if len(il) == 1}
        for a,t in new_toxins.items():
            toxic.append((a,t)) # `t` contains `a`
            del suspects[a]
            for a in suspects:
                if t in suspects[a]:
                    suspects[a].remove(t)

    # "alphabetically by their allergen"
    print("part 2 (dangerous ingredients list):",
          ','.join(t[1] for t in sorted(toxic)))
