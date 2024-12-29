class Body:
    def __init__(self, name):
        self._name = name
        self.parent = None
        self.satellites = set()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._name}>"

bodies = {}

def get_body(name):
    if name not in bodies:
        bodies[name] = Body(name)
    return bodies[name]

def make_orbit(parent, satellite):
    parent = get_body(parent)
    satellite = get_body(satellite)
    parent.satellites.add(satellite)
    satellite.parent = parent

def all_parents(body):
    parent = body.parent
    while parent:
        yield parent
        parent = parent.parent

def go(input):
    orbits = parse.lines(input)
    for orbit in orbits:
        make_orbit(*orbit.split(')'))
    print("part 1 (total direct and indirect orbits",
          sum(len(list(all_parents(b))) for b in bodies.values()))
    if 'YOU' in bodies and 'SAN' in bodies:
        your_parents = list(all_parents(bodies['YOU']))
        santa_parents = list(all_parents(bodies['SAN']))
        total = None
        for i,p in enumerate(your_parents):
            if p in santa_parents:
                total = i + santa_parents.index(p)
                break
            if total is not None:
                break
    print("part 2 (total transfers from you to Santa):",
          total)
                
        
        
