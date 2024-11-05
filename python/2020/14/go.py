mask_re = re.compile('^mask = ([10X]{36})$')
write_re = re.compile(r'^mem\[([0-9]+)\] = ([0-9]+)$')

class Group:
    def __init__(self, mask, writes):
        self.mask = mask
        self.writes = writes

    def part1(self):
        """Generate address, value pairs for writes by part 1 rules."""
        for address, value in self.writes:
            true_value = 0
            for bit in range(36):
                mbit = self.mask[35-bit]
                if mbit == '1':
                    true_value += 2**bit
                elif mbit == 'X':
                    true_value += (2**bit) & value
                else:
                    assert mbit == '0'
            yield address, true_value

    def part2(self):
        """Generate address, value pairs for writes by part 2 rules."""
        def float_addresses(floats):
            if floats:
                for a in float_addresses(floats[1:]):
                    yield a
                    yield floats[0] + a
            else:
                yield 0
            
        for address, value in self.writes:
            true_address = 0
            floating = []
            for bit in range(36):
                mbit = self.mask[35-bit]
                if mbit == '1':
                    true_address += 2**bit
                elif mbit == 'X':
                    floating.append(2**bit)
                else:
                    assert mbit == '0'
                    true_address += (2**bit) & address
            for floated in float_addresses(floating):
                yield floated+true_address, value

def go(input):
    lines = parse.lines(input)
    groups = []
    writes = []
    mask = None
    for l in lines:
        mask_line = mask_re.match(l)
        write_line = write_re.match(l)
        assert mask_line or write_line
        if mask_line:
            if mask and writes:
                groups.append(Group(mask, writes))
            mask = mask_line.group(1)
            writes = []
        if write_line:
            assert mask
            writes.append((int(write_line.group(1)), int(write_line.group(2))))
    if mask and writes:
        groups.append(Group(mask, writes))
    
    mem = {}
    for g in groups:
        for a,v in g.part1():
            mem[a] = v
    print("part 1 (total when masking values):", sum(mem.values()))

    if max(g.mask.count('X') for g in groups) < 20:
        # skip second part for first test when the mask is mostly Xs.
        mem = {}
        for g in groups:
            for a,v in g.part2():
                mem[a] = v
        print("part 2 (total when masking addresses):", sum(mem.values()))
