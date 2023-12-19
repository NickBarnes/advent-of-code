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
                    for (cat, compname, comp, val, next) in self.rules]

def go(input):
    sections = parse.sections(input)
    assert len(sections) == 2
    flows = {f.name:f for l in sections[0] if (f := Flow(l))}
    flows['R'] = Flow('R')
    flows['A'] = Flow('A')
    for f in flows.values():
        f.resolve(flows)
        
    parts = [[int(x) for x in m.groups()] for l in sections[1] if (m := part_re.match(l))]

    total = 0
    for p in parts:
        flow = flows['in']
        while flow.rules:
            for rule in flow.rules:
                if rule[2](p[rule[0]],rule[3]):
                    flow = rule[4]
                    break
            else:
                flow = flow.default
        if flow.name == 'A':
            total += sum(p)
    print("part 1, rating sum of accepted parts:", total)
    
    ways = 0
    queue = [(flows['in'], list((1,4000) for a in range(4)))]
    while queue:
        f,ranges = queue.pop()
        if f.name == 'R':
            continue
        elif f.name == 'A':
            ways += misc.prod(r[1]-r[0]+1 for r in ranges)
            continue
        else:
            for rule in f.rules:
                i = rule[0]
                if rule[1] == '>': # x > 37
                    if ranges[i][1] > rule[3]: # follow this rule ...
                        if rule[3] >= ranges[i][0]:
                            nr = ranges[:]
                            nr[i] = (rule[3]+1, nr[i][1])
                            queue.append((rule[4], nr))
                        else: # always follow this rule
                            queue.append((rule[4], ranges))
                            break
                        # range is split, so go both ways
                        ranges[i] = (ranges[i][0], rule[3])
                else: # a < 2100
                    if ranges[i][0] < rule[3]:
                        if rule[3] <= ranges[i][1]:
                            nr = ranges[:]
                            nr[i] = (nr[i][0], rule[3]-1)
                            queue.append((rule[4], nr))
                        else: # always follow this rule
                            queue.append((rule[4], ranges))
                            break
                        # range is split
                        ranges[i] = (rule[3], ranges[i][1])
            else: # made it to the default case
                queue.append((f.default, ranges))
    print("part 2, acceptable rating combinations:", ways)
