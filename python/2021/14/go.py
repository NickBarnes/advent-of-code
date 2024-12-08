def go(input):
    lines = parse.lines(input)
    template = lines[0]
    
    rule_re = re.compile('([A-Z][A-Z]) -> ([A-Z])$')
    rules = {m.group(1):m.group(2) for l in lines if (m := rule_re.match(l))}
    pair_rules = {k:(k[0]+v,v+k[1]) for k,v in rules.items()}
    
    def apply(pairs):
        newpairs = Counter()
        for p,n in pairs.items():
            for newpair in pair_rules.get(p,[p]):
                newpairs[newpair] += n
        return newpairs
    
    def final_frequencies(template, rounds):
        pairs = Counter(template[i:i+2] for i in range(len(template)-1))
    
        for i in range(rounds):
            pairs = apply(pairs)
    
        counts = Counter()
        for p,n in pairs.items():
            counts[p[0]] += n
            counts[p[1]] += n
        # The above should count every character twice except for the first and last
    
        counts[template[0]] += 1
        counts[template[-1]] += 1
    
        s = [(v // 2,k) for k,v in counts.items()]
        s.sort()
        return s
    
    s = final_frequencies(template, 10)
    
    print(f"part 1 (quantity range after 10 rounds): {s[-1][0]-s[0][0]}.")
    
    s = final_frequencies(template, 40)
    
    print(f"part 2 (quantity range after 40 rounds): {s[-1][0]-s[0][0]}.")
