button_re = re.compile(r"^Button (.): X\+([0-9]+), Y\+([0-9]+)$")
prize_re = re.compile(r"^Prize: X=([0-9]+), Y=([0-9]+)$")

# Extended Euclidean algorithm, useful in the degenerate case (which
# we never actually encounter).

def extended_euclid(a,b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = extended_euclid(b, a % b)
        return g, y, x - y * (a // b)

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
        assert 0 <= self.xa and 0 <= self.ya
        assert 0 <= self.xb and 0 <= self.yb
        assert 0 <= self.xp and 0 <= self.yp
        self.b_denominator = self.xb * self.ya - self.xa * self.yb
        self.degenerate = (self.b_denominator == 0)

    def correct(self):
        self.xp += 10_000_000_000_000
        self.yp += 10_000_000_000_000

    def degenerate_solve(self, testing=False):
        # A and B movements are parallel
        # call the common sub-step (dx, dy)
        dx = math.gcd(self.xa, self.xb) # x sub-step
        ma = self.xa // dx # number of sub-step movements for A
        if self.xp % dx != 0: # wrong granularity to reach prize; no solution
            if testing: print("wrong granularity to reach prize", end='')
            return None

        m = self.xp // dx # number of sub-step movements for prize

        dy = self.ya // ma # y sub-step
        if m * dy != self.yp: # Prize not parallel to A,B; no solution
            if testing: print("prize not parallel to A,B", end='')
            return None

        mb = self.xb // dx # number of sub-step movements for B

        # Now we need to solve the Diophantine equation
        # a.ma + b.mb == m
        # note that ma, mb > 0
        # subject to the constraints a,b >= 0
        # and we need to find the solution with the smallest value of c = 3a+b

        # First find x,y so that ma.x + mb.y = gcd(ma,mb)
        g,x,y = extended_euclid(ma,mb) # g > 0

        a0,b0 = x * (m // g), y * (m // g) # base Diophantine solution

        # other solutions are all a0 + k * (mb // g), b0 - k * (ma // g)
        da, db = mb // g, -ma // g # da > 0, db < 0

        # solution with minimal non-negatve a
        kmin = - (a0 // da)
        a = a0 + kmin * da
        b = b0 + kmin * db

        if b < 0: # minimum A presses still requires negative B presses
            if testing: print("B presses always negative", end='')
            return

        if self.xa > 3 * self.xb:
            # A steps are large; minimise b instead
            k = b // (-db)
            a += k * da
            b += k * db

        assert a * self.xa + b * self.xb == self.xp
        assert a * self.ya + b * self.yb == self.yp
        
        return 3 * a + b, a, b


    def solve(self, testing=False):
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

        if self.degenerate:
            return self.degenerate_solve(testing)
        b_numerator = self.xp * self.ya - self.yp * self.xa
        if b_numerator % self.b_denominator != 0: # b not integral
            if testing: print("non-integral B presses", end='')
            return None
        b = b_numerator // self.b_denominator
        if b < 0: # b negative
            if testing: print("negative B presses", end='')
            return None
        a_numerator = self.xp - b * self.xb
        if a_numerator % self.xa != 0: # a not integral
            if testing: print("non-integral A presses", end='')
            return None
        a = a_numerator // self.xa
        if a < 0: # a negative
            if testing: print("negative A presses", end='')
            return None
        return a * 3 + b, a, b

def cost(machines, testing=False):
    total = 0
    for i,m in enumerate(machines):
        if testing: print(f"machine {i}: ", end='')
        solution = m.solve(testing)
        if solution:
            cost,a,b = solution
            if testing:
                print(f"{a} x A ({m.xa},{m.ya}), {b} x B ({m.xb},{m.yb}) = P ({m.xp},{m.yp}): cost {cost}")
            total += cost
        elif testing:
            print()
    return total

def go(input):
    machines = [Machine(section) for section in parse.sections(input)]
    testing = len(machines) < 20
    print("part 1 (cost with regular machines):",
          cost(machines, testing=testing))
    for machine in machines:
        machine.correct()
    print("part 2 (cost with corrected machines):",
          cost(machines, testing=testing))
