def go(input):
    sections = parse.sections(input)
    assert len(sections) == 2
    rules = []
    for l in sections[0]:
        pages = [int(p) for p in l.split('|')]
        assert len(pages) == 2
        rules.append(pages)

    updates = []
    for l in sections[1]:
        pages = [int(p) for p in l.split(',')]
        updates.append(pages)

    # part 1
    sum = 0
    incorrect = []
    for update in updates:
        for rule in rules:
            if rule[0] not in update or rule[1] not in update:
                continue
            if update.index(rule[0]) > update.index(rule[1]):
                incorrect.append(update)
                break
        else:
            sum += update[len(update) // 2]

    print(f"part 1 (middle pages of incorrect updates): {sum}")

    # part 2
    sum = 0
    for update in incorrect:
        my_rules = [rule for rule in rules if rule[0] in update and rule[1] in update]
        good = False
        while not good: # Is this guaranteed to terminate?
            swaps = 0
            good = True
            for rule in my_rules:
                r1,r2 = rule
                i1, i2 = update.index(r1), update.index(r2)
                if i1 > i2:
                    good = False
                    swaps += 1
                    update[i1], update[i2] = r2, r1 # exchange
        # assert correct
        for rule in my_rules:
            r1,r2 = rule
            i1, i2 = update.index(r1), update.index(r2)
            assert i1 < i2
        sum += update[len(update) // 2]
    print(f"part 2 (middle pages after correcting updates): {sum}")

        
            

                

