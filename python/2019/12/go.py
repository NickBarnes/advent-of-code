moon_re = re.compile(r'^<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>$')

class Moon:
    def __init__(self, vals):
        self._orig = vals
        self.axes = len(vals)
        self.reset()

    def reset(self):
        vals = self._orig
        self.pos = [int(v) for v in vals]
        self.vel = [0 for _ in vals]

    def gravitate(self, other):
        v = []
        for i in range(self.axes):
            dp = other.pos[i] - self.pos[i]
            a = 1 if dp > 0 else -1 if dp < 0 else 0
            v.append(self.vel[i] + a)
        self.vel = v

    def move(self):
        for i in range(self.axes):
            self.pos[i] += self.vel[i]

    # it feels dirty calling any of these "energy"
    def potential(self):
        return sum(abs(p) for p in self.pos)

    def kinetic(self):
        return sum(abs(v) for v in self.vel)

    def energy(self):
        return self.potential() * self.kinetic()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.pos} + {self.vel}>"

def go(input):
    moons = []
    for line in parse.lines(input):
        m = moon_re.match(line)
        assert m
        moons.append(Moon(m.groups()))

    axes = moons[0].axes
    assert all(m.axes == axes for m in moons)

    duration = 100 if AoC.testing else 1000

    def evolve():
        for i,m1 in enumerate(moons):
            for m2 in moons[i+1:]:
                m1.gravitate(m2)
                m2.gravitate(m1)
        for m in moons:
            m.move()

    for t in range(duration):
        evolve()

    print(f"part 1 (total energy after {t+1}):",
          sum(m.energy() for m in moons))

    # To find repeated positions. Observe that the three axes evolve
    # independently, and find a repeat on each axis.
    for m in moons:
        m.reset()
    t = 0
    seen = {}
    repeats = {}
    while len(repeats) < axes:
        for axis in range(axes):
            if axis not in repeats:
                k = (axis, tuple((m.pos[axis], m.vel[axis]) for m in moons))
                if k in seen:
                    repeats[axis] = (seen[k], t)
                else:
                    seen[k] = t
        evolve()
        t += 1

    # It is possible to compute the dynamics in reverse:
    # x(t-1) = x(t)-v(t), v(t-1) = v(t)-a(x(t-1)).  So if t1
    # repeats at t2 then t1-1 repeats at t2-1.  So the first repeat on
    # each axis is of the state at time zero and we don't need to use
    # the Chinese remainder theorem.
    assert all(a == 0 for a,_ in repeats.values())
    print("part 2 (time to first repetition)",
          math.lcm(*(b for _,b in repeats.values())))
    
    # CRT version:
    # divrems = [(b-a, a) for a,b in repeats.values()]
    # div, rem = number.general_chinese_remainder(divrems)
    # if rem == 0:
    #     rem = div
