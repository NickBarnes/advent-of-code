import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))
import walk
import file
import re
import math
from collections import Counter

node_re = re.compile('([1-9A-Z]{3}) = \(([1-9A-Z]{3}), ([1-9A-Z]{3})\)')

class Node:
    def __init__(self, l):
        assert (m := node_re.match(l))
        self.id = m.group(1)
        self.start = self.id.endswith('A')
        self.finish = self.id.endswith('Z')
        self.go = {'L': m.group(2), 'R': m.group(3)}

    def resolve(self, g):
        for d in self.go:
            self.go[d] = g[self.go[d]]

    def __repr__(self):
        return f'<{self.id}>'

def steps(dirs, node):
    n = 0
    l = len(dirs)
    while not node.finish:
        node = node.go[dirs[n % l]]
        n += 1
    return n

def loop_len(node, dirs):
    history = {}
    finishes = set()
    l = len(dirs)
    step = 0
    while True:
        k = (node, step % l)
        if k in history:
            to_loop = history[k] # first time we got here
            loop_len = step - history[k] # how long ago was that
            break
        else:
            history[k] = step
        node = node.go[dirs[step % l]]
        step += 1
        if node.finish:
            finishes.add(step)

    # offsets of finishing nodes within the loop.
    finishes = set(s-to_loop for s in finishes)
    # it turns out that the problem dataset is very constrained:
    # (a) no ghost reaches an exit before its loop
    assert all(s > 0 for s in finishes)
    # (b) each ghost only passes through a single exit on its loop;
    # (c) it does so on its Nth step, where N is the loop length
    assert list(finishes) == [loop_len - to_loop]
    # Without these assumptions, we would have to do much more work
    # (and would need the values in the set `finishes`).
    return loop_len

def go(filename):
    print(f"results from {filename}:")
    sections = file.sections(filename)
    assert len(sections) == 2
    assert len(sections[0]) == 1
    directions = sections[0][0]
    assert len(Counter(directions)) <= 2 # 'L' and 'R'
    graph = {n.id:n for l in sections[1] if (n := Node(l))}
    for n in graph.values():
        n.resolve(graph)

    if 'AAA' in graph:
        print("part 1:", steps(directions, graph['AAA']))
    else:
        print("part 1: no 'AAA' in graph")

    if 'input' in filename:
        print("part 2:", math.lcm(*(loop_len(n, directions)
                                    for n in graph.values() if n.start)))
    else:
        print("part 2 not done on test input.")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
