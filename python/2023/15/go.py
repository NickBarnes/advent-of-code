def hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h

box_re = re.compile('([a-z]+)(-|=([0-9]+))')

def run(cmds):
    boxes = [[] for i in range(256)]
    for c in cmds:
        m = box_re.match(c)
        assert m
        label = m.group(1)
        h = hash(label)
        lenses = boxes[h]
        if m.group(2) == '-':
            boxes[h] = [(l,f) for l,f in lenses if l != label]
        else:
            focal = int(m.group(3))
            for i,(l,_) in enumerate(lenses):
                if l == label:
                    lenses[i] = (label,focal)
                    break
            else: # not found
                lenses.append((label,focal))
    return sum((i + 1) * (j + 1) * f
               for i,box in enumerate(boxes)
               for j,(_,f) in enumerate(box))

def go(input):
    lines = parse.lines(input)
    assert len(lines) == 1
    cmds = lines[0].split(',')
    print("part 1, sum of hashes:", sum(hash(w) for w in cmds))
    print("aprt 2, focussing power:", run(cmds))
        
    
