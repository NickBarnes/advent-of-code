field_re = re.compile('^([a-z ]+): (.*)$')
group_re = re.compile('([0-9]+)-([0-9]+)')


def valid_field(field, number):
    """Return True if `number` is in a range of `field`, False otherwise."""
    return any(a <= number <= b for (a,b) in field[1])

def any_valid(fields, number):
    """Returns True if `number` is in one of the ranges of `field`,
    False otherwise."""
    return any(valid_field(field, number) for field in fields)

def impossible_fields(fields, number):
    """Returns the set of field names for which `number` is not in
    any of the ranges."""
    return set(field[0] for field in fields if not valid_field(field, number))

def go(input):
    # Parsing
    sections = parse.sections(input)
    assert len(sections) == 3
    fields = []
    for field in sections[0]:
        m = field_re.match(field)
        assert m
        name = m.group(1)
        ranges = []
        groups = m.group(2).split(' or ')
        for g in groups:
            m = group_re.match(g)
            assert m
            first,last = int(m.group(1)),int(m.group(2))
            assert first < last
            assert not ranges or ranges[-1][-1] < first
            ranges.append((first,last))
        fields.append((name, ranges))
    field_names = set(field[0] for field in fields)

    assert sections[1][0] == 'your ticket:'
    assert len(sections[1]) == 2
    your_ticket = [int(s) for s in sections[1][1].split(',')]

    assert sections[2][0] == 'nearby tickets:'
    assert len(sections[2]) > 1
    nearby_tickets = [[int(s) for s in l.split(',')] for l in sections[2][1:]]
    assert all(len(t) == len(your_ticket) for t in nearby_tickets)
        
    print("part 1 (sum of invalid values):",
          sum(v for t in nearby_tickets for v in t if not any_valid(fields, v)))
    valid_tickets = [t for t in nearby_tickets if all(any_valid(fields, v) for v in t)]
    
    possible = {}
    for i in range(len(your_ticket)):
        exclude = set.union(*(impossible_fields(fields, t[i]) for t in valid_tickets))
        possible[i] = field_names - exclude
    
    definite = {}
    while possible:
        for i,s in list(possible.items()):
            if len(s) == 1:
                field = s.pop()
                definite[i] = field
                del possible[i]
                for j,t in list(possible.items()):
                    if field in t:
                        t.remove(field)
                        assert t
    
    your_ticket = {definite[i]:your_ticket[i] for i in range(len(fields))}

    if any(k.startswith('departure ') for k in your_ticket):
        print("part 2 (product of departure fields):",
              misc.prod(v
                        for k,v in your_ticket.items()
                        if k.startswith('departure ')))
