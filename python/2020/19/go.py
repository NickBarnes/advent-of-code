import itertools

rule_re = re.compile('^([0-9]+): ("([a-z])"|([0-9 |]+))$')

def check(rules, rule, s, i):
    """Generate the positions after any match of `s[i:]` with `rule`
    from the ruleset `rules`.
    """

    if i >= len(s):
        return
    if isinstance(rule, str):
        if s.startswith(rule, i):
            yield i+len(rule)
        return
    # list of lists:
    for l in rule:
        posns = [i] # list of current positions
        for item in l:
            posns = list(itertools.chain(*(check(rules, rules[item], s, pos)
                                           for pos in posns)))
            if not posns : # failed to match item at any possible position
                break
        else: # all items succeeded, we are done
            for p in posns:
                yield p

def go(input):
    # Parse input
    sections = parse.sections(input)
    assert len(sections) == 2
    matches = [rule_re.match(line) for line in sections[0]]
    assert all(matches)
    rules = {}
    for r in matches:
        id = int(r.group(1))
        if r.group(3):
            rules[id] = r.group(3)
        else:
            lists = r.group(4).split('|')
            rules[id] = [[int(r) for r in l.split()] for l in lists]

    # Solution
    print("part 1 (how many strings match rule 0):",
          sum(1 for s in sections[1] if len(s) in check(rules, rules[0], s, 0)))

    # amend rules for part 2
    rules[8] = [[42],[42,8]]
    rules[11] = [[42,31],[42,11,31]]

    print("part 2 (how many strings match after amending rules 8 and 11):",
          sum(1 for s in sections[1] if len(s) in check(rules, rules[0], s, 0)))
