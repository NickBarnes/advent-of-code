import operator

class Wire:
    def __init__(self, name):
        self.name = name
        self.sinks = set()
        self.source = None
        self.tentative = None
        self.bad = False

    def set(self, value, state):
        state[self] = value
        for gate in self.sinks:
            gate.trigger(state)
    
    def __repr__(self):
        return f'<{self.name}>'
    
wires = {}
def get_wire(name):
    if name not in wires:
        wires[name] = Wire(name)
    return wires[name]

def wires_with(c):
    return {name:wires[name] for name in wires if name.startswith(c)}

gate_re = re.compile(r'^([a-z0-9]+) (AND|OR|XOR) ([a-z0-9]+) -> ([a-z0-9]+)$')

class Gate:
    def __init__(self, line):
        m = gate_re.match(line)
        assert m
        self.input1 = get_wire(m.group(1))
        self.input2 = get_wire(m.group(3))
        self.inputs = {self.input1, self.input2}
        self.output = get_wire(m.group(4))
        if m.group(2) == 'AND':
            self.fun, self.sym = operator.and_, '&'
        elif m.group(2) == 'OR':
            self.fun, self.sym = operator.or_, '|'
        elif m.group(2) == 'XOR':
            self.fun, self.sym = operator.xor, '^'
        self.input1.sinks.add(self)
        self.input2.sinks.add(self)
        assert self.output.source is None
        self.output.source = self

    def trigger(self, state):
        if self.input1 in state and self.input2 in state:
            res = self.fun(state[self.input1], state[self.input2])
            state[self] = res
            self.output.set(res, state)

    def __repr__(self):
        return f'<{self.input1.name} {self.sym} {self.input2.name}>'

init_re = re.compile(r'^([a-z0-9]+): ([01])$')

def go(input):
    global wires
    wires = {}
    inits, gates = parse.sections(input)
    gates = [Gate(gate) for gate in gates]
    state = {}
    for init in inits:
        m = init_re.match(init)
        assert m
        get_wire(m.group(1)).set(m.group(2) == '1', state)

    # part 1
    output_wires = wires_with('z')
    total, bit = 0, 0
    while output_wires:
        name = f'z{bit:02}'
        total += state[output_wires[name]] << bit
        del output_wires[name]
        bit += 1
    print("part 1 (value on z wires):", total)

    # Part 2
    #
    # Started with some manual analysis of the circuit; see long
    # comment at the end.  To find swapped wires, start by tentatively
    # identifying wires working forwards from the input, and check
    # that each one goes into the right number and type of gates.
    # Then we can check more of the graph topology.

    if AoC.testing:
        print("No part 2: test cases too different from main problem")
        return

    mainx = {int(name[1:]): wire for name, wire in wires_with('x').items() if name != 'x00'}
    mainy = {int(name[1:]): wire for name, wire in wires_with('y').items() if name != 'y00'}
    x00 = wires['x00']
    y00 = wires['y00']
    in00 = {x00,y00}

    # There are the same x and y indices
    assert set(mainx) == set(mainy)
    main_in = {bit:{mainx[bit],mainy[bit]} for bit in mainx}
    # Each x and y goes into the same 2 sinks, & and ^, and nothing else
    assert all(len(wire.sinks) == 2 for wire in in00)
    assert all(any(sink.sym == sym for sink in wire.sinks) for sym in '&^' for wire in in00)
    assert all(sink.inputs == in00 for wire in in00 for sink in wire.sinks)
    assert all(len(wire.sinks) == 2 for ins in main_in.values() for wire in ins)
    assert all(any(sink.sym == sym for sink in wire.sinks) for ins in main_in.values() for wire in ins for sym in '&^')
    assert all(sink.inputs == ins for ins in main_in.values() for wire in ins for sink in wire.sinks)

    # a_i     = x_i & y_i
    # d_i     = x_i ^ y_i
    # b_i     = c_i & d_i
    # z_i     = c_i ^ d_i
    # c_{i+1} = b_i | a_i

    a, b, c, d, z = {},{},{},{},{}

    bad = set()

    def fail(wire, reason):
        bad.add(wire)
        if AoC.verbose:
            print(f"{wire.name}: {reason}")
        wire.bad = True
        
    def check_not_z(wire):
        if wire.name.startswith('z'):
            fail(wire, f"({wire.expr}) should not be a z")

    # Carry bits should either be z45 or input to an AND and a XOR,
    # both with the same other input.
    def check_c(wire, i):
        if wire.tentative == 'c45':
            if wire.name != 'z45':
                fail(wire, "should be z45")
                return
        check_not_z(wire)
        if len(wire.sinks) != 2:
            fail(wire, f"not a carry as it has {len(wire.sinks)} sinks")
            return
        if not all(any(sink.sym == sym for sink in wire.sinks) for sym in '&^'):
            fail(wire, "not a carry as it doesn't have AND and XOR sinks")
            return

    # an 'a' should be input to a single 'OR' gate.
    def check_a(wire, i):
        check_not_z(wire)
        if len(wire.sinks) != 1:
            fail(wire, f"not an 'a' as it has {len(wire.sinks)} sinks")
            return
        if not all(s.sym == '|' for s in wire.sinks):
            fail(wire, "not an 'a' as it has a sink which is not OR")

    # a 'b' should be input to a single 'OR' gate.
    def check_b(wire, i):
        check_not_z(wire)
        if len(wire.sinks) != 1:
            fail(wire, f"not an 'b' as it has {len(wire.sinks)} sinks")
            return
        if not all(s.sym == '|' for s in wire.sinks):
            fail(wire, "not an 'b' as it has a sink which is not OR")

    # a 'z' should have a name starting with 'z' and not be input to anything.
    def check_z(wire, i):
        if not wire.name == wire.tentative:
            fail(wire, f"not named {wire.tentative}")
        if wire.sinks:
            fail(wire, f"not a z as it has {len(wire.sinks)} sinks")

    # a 'd' should be input to an AND and a XOR, both with the same
    # other input (which should be the carry from the previous input).
    def check_d(wire, i):
        check_not_z(wire)
        if len(wire.sinks) != 2:
            fail(wire, f"not a 'd' as it has {len(wire.sinks)} sinks")
            return
        if not all(any(sink.sym == sym for sink in wire.sinks) for sym in '&^'):
            fail(wire, "not a 'd' as it doesn't have AND and XOR sinks")
            return
        # TODO: check that those sinks both have the same other inputs (which should be the right carry)
       
    c[0] = [s.output for s in x00.sinks if s.sym == '&'][0]
    c[0].expr = 'x00 & y00'
    c[0].tentative = "c00"
    check_c(c[0],0)

    for i in range(1,len(mainx)):
        xi = mainx[i]
        a[i] = [s.output for s in xi.sinks if s.sym == '&'][0]
        a[i].expr = f"x{i:02} & y{i:02}"
        a[i].tentative = f"a{i:02}"
        check_a(a[i],i)
        d[i] = [s.output for s in xi.sinks if s.sym == '^'][0]
        d[i].tentative = f"d{i:02}"
        d[i].expr = f"x{i:02} ^ y{i:02}"
        check_d(d[i],i)
        if not d[i].bad:
            b[i] = [s.output for s in d[i].sinks if s.sym == '&'][0]
            b[i].tentative = f"b{i:02}"
            b[i].expr = f"c{i:02} & d{i:02}"
            check_b(b[i], i)
            z[i] = [s.output for s in d[i].sinks if s.sym == '^'][0]
            z[i].tentative = f"z{i:02}"
            z[i].expr = f"c{i:02} ^ d{i:02}"
            check_z(z[i], i)
        if not a[i].bad:
            c[i+1] = [s.output for s in a[i].sinks][0]
            c[i+1].tentative = f"c{i+1:02}"
            c[i+1].expr = f"b{i:02} ^ a{i:02}"
            check_c(c[i+1], i)

    # Plenty more checks we could do (basically topology: Does each
    # c/d gate take both a c and the appropriate d? Does each a/b gate
    # take the matching a and b?) but disappointingly this turns out
    # to be enough.

    assert len(bad) == 8
    print("part 2 (names of swapped wires):",
          ','.join(sorted((wire.name for wire in bad))))

# We should have an adder circuit. Sample a single bit position,
# 30, by hand, and let's see where the wires go (if this one turns
# out not to be a one-bit full adder we'll look at another):
#
# x30 AND y30 -> bjj
# x30 XOR y30 -> cmf
#
# qnt XOR cmf -> z30
# cmf AND qnt -> gbf
#
# gbf OR bjj -> rqp
#
# x30 y30 qnt bjj cmf z30 gbf rqp
#   0   0   0   0   0   0   0   0
#   0   0   1   0   0   1   0   0
#   0   1   0   0   1   1   0   0
#   0   1   1   0   1   0   1   1
#   1   0   0   0   1   1   0   0
#   1   0   1   0   1   0   1   1
#   1   1   0   1   0   0   0   1
#   1   1   1   1   0   1   0   1

# This is indeed a full one-bit adder circuit; qnt is the carry bit
# from the previous position (call that c<N>), rqp is the carry bit to
# the next position (c<N+1>), and bjj, cmf, and gpf are intermediate
# results.
# 
# So we should see this pattern for every position from 01 to 44:

# x<N> AND y<N> -> a<N> # and1
# x<N> XOR y<N> -> d<N> # xor1
#
# c<N> AND d<N> -> b<N> # and2
# c<N> XOR d<N> -> z<N> # xor2
#
# b<N> OR a<N> -> c<N+1> # or

# For position zero, the gates should be simpler, as c<0> is 0:

# x00 AND y00 -> c01
# x00 XOR y00 -> z00 [Note, this gate does indeed exist]

# c45 is just z45.

# So that would be the correct set of gates, and there should be 222
# of them. That is the actual number of gates.


