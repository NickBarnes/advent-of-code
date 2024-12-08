import operator

flow_re = re.compile('([a-z]+){(.*)}')
rule_re = re.compile('([xmas])([><])([0-9]+):([a-z]+|A|R)')
part_re = re.compile('{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)}')

cats = {c:i for i,c in enumerate('xmas')}
op_fns = {'>':operator.gt, '<':operator.lt}

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
        self.rules = [rule_re.match(rule).groups() for rule in rules[:-1]]
        self.default = rules[-1]

    def resolve(self, flows):
        self.default = flows[self.default]
        self.rules=[(cats[cat], op, op_fns[op], int(crit), flows[next])
                    for cat, op, crit, next in self.rules]
                      
    def apply(self, vals):
        for cat, _, fn, crit, next in self.rules:
            if fn(vals[cat], crit):
                return next
        return self.default

    def apply_ranges(self, ranges):
        for cat, op, _, crit, next in self.rules:
            nr = ranges[:]
            lo,hi = ranges[cat]
            if op == '>':
                nr[cat] = (max(crit+1, lo), hi)
                ranges[cat] = (lo, min(hi, crit))
            else:
                nr[cat] = (lo, min(hi, crit-1))
                ranges[cat] = (max(crit, lo), hi)
            yield next, nr
        yield self.default, ranges

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
