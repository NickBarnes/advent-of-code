line_re = re.compile('^([a-z ]+) bags contain (.*)$')
none_text = 'no other bags.'
item_re = re.compile('^([0-9]+) ([a-z ]+) bags?\\.?$')

def go(input):
    contents = {}
    for l in parse.lines(input):
        m = line_re.match(l)
        col = m.group(1)
        rest = m.group(2)
        contents[col] = []
        if rest == none_text:
            continue
        for item in rest.split(', '):
            m = item_re.match(item)
            contents[col].append((int(m.group(1)), m.group(2)))
    containers = {inner: {outer for outer in contents
                          if any(x[1] == inner for x in contents[outer])}
                  for inner in contents}

    start = 'shiny gold'
    outers = set()
    grey = set([start])
    seen = set()
    while grey:
        col = grey.pop()
        for outer in containers.get(col, []):
            outers.add(outer)
            if outer not in seen:
                seen.add(outer)
                grey.add(outer)
    print("part 1 (how many outer bag colours contain a shiny gold bag):",
          len(outers))

    weight = dict()
    left = set(contents)
    while left:
        for col in set(left):
            if all(x[1] in weight for x in contents[col]):
                left.remove(col)
                weight[col] = sum(weight[x[1]]*x[0] for x in contents[col]) + 1

    print("part 2 (how many bags in a shiny gold bag):",
          weight['shiny gold'] - 1)
