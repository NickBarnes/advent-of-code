import operator

flow_re = re.compile('([a-z]+){(.*)}')
rule_re = re.compile('([xmas])([><])([0-9]+):([a-z]+|A|R)')
part_re = re.compile('{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)')

cats = {c:i for i,c in enumerate('xmas')}
comps = {'>':operator.gt, '<':operator.lt}

class Flow:
    def __init__(self, s):
        if s in 'RA':
            self.rules = []
            self.default = s
            self.name = s
            return
        m = flow_re.match(s)
        self.name = m.group(1)
        rules = m.group(2).split(',')
        self.rules = [(cats[m.group(1)], m.group(2), comps[m.group(2)],
                       int(m.group(3)), m.group(4))
                      for rule in rules[:-1] if (m := rule_re.match(rule))]
        self.default = rules[-1]

    def resolve(self, flows):
        self.default = flows[self.default]
        self.rules=[(cat, compname, comp, val, flows[next])
                    for cat, compname, comp, val, next in self.rules]

    def apply(self, vals):
        for cat, _, comp, val, next in self.rules:
            if comp(vals[cat],val):
                return next
        return self.default

    def apply_ranges(self, ranges):
        for cat, compname, _, val, next in self.rules:
            nr = ranges[:]
            if compname == '>': # x > 37
                nr[cat] = (max(val+1, nr[cat][0]), nr[cat][1])
                ranges[cat] = (ranges[cat][0], min(ranges[cat][1], val))
            else: # a < 2100
                nr[cat] = (nr[cat][0], min(ranges[cat][1], val-1))
                ranges[cat] = (max(val, ranges[cat][0]), ranges[cat][1])
            yield (next, nr)
        else: # made it to the default case
            yield (self.default, ranges)

def go(input):
    sections = parse.sections(input)
    assert len(sections) == 2
    flows = {f.name:f for l in sections[0] if (f := Flow(l))}
    flows['R'] = Flow('R')
    flows['A'] = Flow('A')
    for f in flows.values():
        f.resolve(flows)
        
    parts = [[int(x) for x in m.groups()]
             for l in sections[1] if (m := part_re.match(l))]

    total = 0
    for part in parts:
        flow = flows['in']
        while flow.rules:
            flow = flow.apply(part)
        if flow.name == 'A':
            total += sum(part)
    print("part 1, rating sum of accepted parts:", total)
    
    ways = 0
    queue = [(flows['in'], list((1,4000) for cat in range(4)))]
    while queue:
        f, ranges = queue.pop()
        if any(r[0] > r[1] for r in ranges): # empty range
            continue
        if f.name == 'R':
            continue
        elif f.name == 'A':
            ways += misc.prod(r[1]-r[0]+1 for r in ranges)
        else:
            queue += list(f.apply_ranges(ranges))
    print("part 2, acceptable rating combinations:", ways)
