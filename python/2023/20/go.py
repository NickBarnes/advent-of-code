class Gate:
    def __init__(self, s):
        self.state = False
        self.inputs = {}
        self.outputs = []
        parts = s.split(' -> ')
        self.r = parts[0]
        if len(parts) == 1: # test gate, button, etc
            self.name = parts[0]
            self.process = self.test_gate
            return
        name, outputs = parts
        if name[0] == '&':
            self.name = name[1:]
            self.process = self.conjunction
        elif s[0] == '%':
            self.name = name[1:]
            self.process = self.flipflop
        else: # broadcaster
            self.name = name
            self.process = self.broadcast
        self.outputs = outputs.split(', ')

    def resolve(self, gates):
        for g in self.outputs:
            if g not in gates: # "for testing purposes"
                gates[g] = Gate(g)
            gates[g].inputs[self.name] = False

    def reset(self):
        self.inputs = {g:False for g in self.inputs}
        self.state = False

    def __repr__(self):
        return self.r

    # Different kinds of gate are distinguished by their
    # `process` function, which is one of the following:
    def conjunction(self, pulse, source):
        self.inputs[source] = pulse
        p = not all(self.inputs.values())
        return [(self.name,p,g) for g in self.outputs]

    def broadcast(self, pulse, source):
        assert not pulse
        assert source == 'button'
        return [(self.name,False,g) for g in self.outputs]

    def flipflop(self, pulse, source):
        if not pulse:
            self.state = not self.state
            return [(self.name,self.state,g) for g in self.outputs]
        else:
            return []

    def test_gate(self, pulse, source):
        return []

# Checks that a sub-circuit behaves in the expected manner:
#
# - the output gate is always low before a button push.
# 
# - rising edges of the output gate always happen on the same tick number
#   after the most recent button push.
# 
# - the same for falling edges.
# 
# - the output gate will eventually rise more than once (if not then
#   this function loops forever).
#
# - Each time the output gate rises, the state of the whole
#   sub-circuit is the same (so it does so on a loop).
#
# Returns the number of button pushes before the first rising edge,
# the number of button pushes in the loop, and the rising/falling edge
# tick numbers (for consistency checking with other sub-circuits).

def pushes_loop(fg, gates, out_gate, sub_circuit):
    edges = {}
    last_state = None
    last = None
    for g in gates.values():
        g.reset()
    pushes = 0
    output = False
    while True:
        pulses = [('broadcaster', False, fg)]
        pushes += 1
        ticks = 0
        while pulses:
            new_pulses = []
            for s,p,d in pulses:
                if s == out_gate and p != output:
                    if p in edges:
                        # output gate changes on consistent ticks
                        assert ticks == edges[p]
                    edges[p] = ticks
                    output = p
                    if p: # rising edge
                        state = list((g, gates[g].state,
                                      sorted(gates[g].inputs.items()))
                                     for g in sorted(sub_circuit))
                        if last_state:
                            # sub-circuit state is always the same
                            # on a rising edge, so we know it's a
                            # fixed-length cycle.
                            assert state == last_state
                            return last, pushes-last, edges
                        last = pushes
                        last_state = state
                new_pulses += gates[d].process(p,s)
            pulses = new_pulses
            ticks += 1
        assert output is False # output gate always low before a push.

def go(input):
    lines = parse.lines(input)
    gates = {g.name:g for line in lines if (g := Gate(line))}
    gates['button'] = Gate('button -> broadcaster')
    for g in list(gates.values()):
        g.resolve(gates)
    
    lows, highs = 0, 0
    for i in range(1000):
        pulses = [('button', False, 'broadcaster')]
        while pulses:
            lows += sum(1 for _,p,_ in pulses if not p)
            highs += sum(1 for _,p,_ in pulses if p)
            new_pulses = []
            for s,p,d in pulses:
                new_pulses += gates[d].process(p,s)
            pulses = new_pulses
    print("part 1, product of low and high pulses:", lows * highs)

    if 'rx' not in gates:
        print("no part 2: no 'rx' gate.")
        return

    # Part 2 asks "How many button pushes until gate 'rx' receives a
    # low pulse.  The general case is clearly far too hard (Halting
    # Problem etc), so this must depend on the structure of the
    # circuit.
    # 
    # By observation, the 'rx' gate has one input, which is a
    # conjunction of four other gates and only has 'rx' as
    # output. Call this last gate `last_gate`, and its four inputs the
    # "output gates" (`output_gates`). Each output gate is a
    # conjunction with a single output. This code checks these
    # observations.
    #
    # Interpreting the problem description with these observations, we
    # want the number of button pushes until last_gate outputs a low
    # pulse, which is the number of button pushes until the most
    # recent output from each output gate is a high pulse.

    last_gates = [g.name for g in gates.values() if 'rx' in g.outputs]
    assert len(last_gates) == 1 # one last gate
    last_gate = last_gates[0]
    assert gates[last_gate].r[0] == '&'       # conjunction
    assert len(gates[last_gate].outputs) == 1 # only outputs to 'rx'
    output_gates = set(gates[last_gate].inputs)
    assert len(output_gates) == 4                                # four inputs
    assert all(gates[g].r[0] == '&' for g in output_gates)       # each a conjunction
    assert all(len(gates[g].outputs) == 1 for g in output_gates) # with one output

    # Also by observation, the broadcaster has 4 outputs ("the first
    # gates", `first_gates`), each of which drives a sub-circuit which
    # has nothing in common with the other sub-circuits except that it
    # drives one of the output gates (and thence the last gate and
    # 'rx'). This code finds the sub-circuits and asserts these
    # invariants.
    #
    # Again, interpreting the problem description, we want the number
    # of button pushes until *some tick* on which the most recent
    # output from each sub-circuit's output gate is a high pulse. It's
    # possible that different sub-circuits push the output high after
    # different numbers of ticks on different button push counts; we
    # need a button push count on which all the different sub-citcuit
    # outputs are high on the same tick.

    first_gates = gates['broadcaster'].outputs
    sub_output = {}
    sub_circuits = {}
    for fg in first_gates:
        for g in gates.values():
            g.reset()
        sub_gates = set()
        grey = set([fg])
        while grey:
            gate = grey.pop()
            if gate not in sub_gates:
                sub_gates.add(gate)
                grey |= set(gates[gate].outputs)
        # each sub-circuit drives a single output gate
        assert len(sub_gates & output_gates) == 1 
        sub_output[fg] = list(sub_gates & output_gates)[0]
        sub_circuits[fg] = sub_gates - set(['rx', last_gate])
    
    # All the output gates are driven by sub-circuits
    assert output_gates == set(sub_output.values())
    # Every gate in the whole circuit belongs to at least one sub-circuit
    assert set(gates) == (set(g for sg in sub_circuits.values() for g in sg) |
                          set('button broadcaster rx'.split()) |
                          set([last_gate]))
    # Corresponding set sizes means that there are no overlaps.
    assert len(gates) == (sum(len(sc) for sc in sub_circuits.values())
                          + 4) # button broadcaster rx last_gate 

    # Observing the behaviour of each sub-circuit (this is mostly done
    # by the `pushes_loop` function).
    #
    # - The output gate is always low before a button push.
    # 
    # - The output gate only goes high on specific button pushes. The
    # number of ticks within a button push on which the output gate
    # goes high, and then low, are the same for each sub-circuit (3
    # and 5 respectively, FWIW). So we don't have to worry about tick
    # co-ordination between sub-circuits.
    # 
    # - Every time the output gate of a sub-circuit goes high, the
    # state of the sub-circuit (all flip-flops, all conjunctions) is
    # the same.
    #
    # - For any given sub-circuit, the number of button pushes before
    # the first rising edge, and the number of button pushes between
    # rising edges, is the same (if this were not true we'd have to
    # use the Chinese Remainder Theorem).
    #
    # So the number of button pushes before all output gates rise
    # together is simply the LCM of the numbers of button pushes
    # beween rising edges for the different sub-circuits.

    edge_ticks = {}
    cycles = {}
    for fg in first_gates:
        first, loop, edges = pushes_loop(fg, gates, sub_output[fg], sub_circuits[fg])
        assert first == loop
        for out in True, False:
            # The sub-circuit drives its output gate in both directions
            assert out in edges
            if out in edge_ticks:
                # All sub-circuits drive their output gates on the same ticks.
                assert edges[out] == edge_ticks[out]
            edge_ticks[out] = edges[out]
        cycles[fg] = loop

    print("part 2, button pushes until rx receives a low pulse:",
          math.lcm(*cycles.values()))
