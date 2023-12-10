import sys
import os
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))

import walk
import file

def go(filename):
    print(f"results from {filename}:")
    sections = file.sections(filename)
    lines = sections[0]
    answer = None
    if len(sections) == 2: # test with given solution to part 2
        answer = int(sections[1][0])
    graph = {}
    for j,l in enumerate(lines):
        for i,c in enumerate(l):
            if c == '-':
                graph[(i,j)] = ((i-1,j),(i+1,j))
            elif c == '|':
                graph[(i,j)] = ((i,j-1),(i,j+1))
            elif c == 'F':
                graph[(i,j)] = ((i,j+1),(i+1,j))
            elif c == '7':
                graph[(i,j)] = ((i,j+1),(i-1,j))
            elif c == 'J':
                graph[(i,j)] = ((i,j-1),(i-1,j))
            elif c == 'L':
                graph[(i,j)] = ((i,j-1),(i+1,j))
            elif c == 'S':
                start=(i,j)
                graph[start] = []
    # figure out graph neighbours of start point
    for k in graph:
        if start in graph[k]:
            graph[start].append(k)
    assert len(graph[start]) == 2 # rubric promises this

    # part 1: go around the loop from S, in both directions at once.
    dist = {}
    visited = set()
    d = 0
    at = set([start])
    while at:
        for node in at:
            dist[node] = d
            visited.add(node)
        d += 1
        at = list(set(n for node in at for n in graph[node]) - visited)
    m = max(dist.values())
    print(f"part 1: max distance on loop is {m}")
    # find locations inside loop using winding number
    loop = defaultdict(set)
    for (i,j) in dist:
        loop[i].add(j)
    in_loop = 0
    for i in loop: # Look down each column in the loop
        rows = sorted(loop[i])
        outside = True # start outside
        for k in range(len(rows)):
            j = rows[k] # (i,j) is on the loop
            neighbours = graph[(i,j)]
            if (i-1,j) in neighbours: # '-' or 'J' or '7'
                if (i+1, j) in neighbours: # '-'
                    outside = not outside
                elif (i,j-1) in neighbours: # 'J'
                    if not from_left: # this section of loop came from the right
                        outside = not outside
                else: # '7'
                    from_left = True
            elif (i+1, j) in neighbours: # 'F' or 'L'
                if (i,j-1) in neighbours: # 'L'
                    if from_left:
                        outside = not outside
                else: # 'F'
                    from_left = False
            if not outside:
                # how many cells in this column before next loop cell?
                in_loop += rows[k+1] - 1 - j
                    
    print(f"part 2: {in_loop} cells contained by the loop")
    if answer:
        if in_loop == answer:
            print("Correct!")
        else:
            print("Incorrect!")
            
    
if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
