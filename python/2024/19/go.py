def go(input):
    towels, designs = parse.sections(input)
    assert len(towels) == 1
    towels = set(t.strip() for t in towels[0].split(','))
    
    memo = {'':1}
    def possibilities(design):
        if design in memo:
            return memo[design]
        res =  sum(possibilities(design[len(t):])
                   for t in towels
                   if design.startswith(t))
        memo[design] = res
        return res

    print("part 1 (possible designs):",
          sum(1 for d in designs if possibilities(d)))
    print("part 2 (towel arrangements):",
          sum(possibilities(d) for d in designs))
