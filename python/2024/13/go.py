button_re = re.compile(r"^Button (.): X\+([0-9]+), Y\+([0-9]+)$")
prize_re = re.compile(r"^Prize: X=([0-9]+), Y=([0-9]+)$")

class Machine:
    def __init__(self, section):
        assert len(section) == 3
        ba = button_re.match(section[0])
        bb = button_re.match(section[1])
        p = prize_re.match(section[2])
        assert ba and bb and p
        assert ba.group(1) == 'A' and bb.group(1) == 'B'
        self.xa, self.ya = int(ba.group(2)),int(ba.group(3))
        self.xb, self.yb = int(bb.group(2)),int(bb.group(3))
        self.xp, self.yp = int(p.group(1)), int(p.group(2))

    def solve(self):
        #   a.xa    + b.xb    == xp
        # so (multiply by ya)
        #   a.xa.ya + b.xb.ya == xp.ya       ... (1)
        #   a.ya    + b.yb    == yp
        # so (multiply by xa)
        #   a.ya.xa + b.yb.xa == yp.xa       ... (2)
        # Then subtract (2) from (1):
        #   b(xb.ya-yb.xa) = xp.ya-yp.xa
        #   b = (xp.ya-yp.xa)/(xb.ya-yb.xa)
        # and of course  
        #   a = (xp - b * xb)/xa
        # if either a or b is not integral, there is no solution

        b_numerator = self.xp * self.ya - self.yp * self.xa
        b_denominator = self.xb * self.ya - self.xa * self.yb
        if b_numerator % b_denominator != 0: # b not integral
            return None
        b = b_numerator // b_denominator
        if b < 0: # b negative
            return None
        a_numerator = self.xp - b * self.xb
        if a_numerator % self.xa != 0: # a not integral
            return None
        a = a_numerator // self.xa
        if a < 0: # a negative
            return None
        return a * 3 + b, a, b

def cost(machines):
    total = 0
    for m in machines:
        solution = m.solve()
        if solution:
            cost,a,b = solution
            total += cost
    return total

def go(input):
    machines = [Machine(section) for section in parse.sections(input)]
    print("part 1 (cost with regular machines):", cost(machines))
    for machine in machines:
        machine.xp += 10_000_000_000_000
        machine.yp += 10_000_000_000_000
    print("part 2 (cost with corrected machines):", cost(machines))
