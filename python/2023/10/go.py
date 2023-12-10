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
    # parse graph. Note: this will include many nodes not on the loop.
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
    graph[start] = [k for k in graph if start in graph[k]]
    assert len(graph[start]) == 2 # rubric promises this

    # part 1: go around the loop from S, in both directions at once.
    visited = set()
    d = 0
    at = set([start])
    while at:
        for node in at:
            visited.add(node)
        d += 1
        at = list(set(n for node in at for n in graph[node]) - visited)
    print(f"part 1: max distance on loop is {d-1}")

    # part 2: how many cells contained inside loop
    loop = defaultdict(set) # column -> set(rows of cells in loop)
    for (i,j) in visited:
        loop[i].add(j)
    in_loop = 0
    for i in loop: # Look down each column
        # loop cells in any one column are either '-',
        # or sequences of | preceded by F/7 and followed by J/L.
        # - or |...J or 7...L cross the column; other sequences do not.
        rows = sorted(loop[i]) # all loop cells in this column
        inside = False # start outside
        for j, j2 in zip(rows, rows[1:]):
            neighbours = graph[(i,j)]
            if (i-1,j) in neighbours: # '-' or 'J' or '7'
                if (i+1, j) in neighbours: # '-'
                    inside = not inside
                elif (i,j-1) in neighbours: # 'J'
                    if not from_left: # the loop came from the right
                        inside = not inside
                else: # '7'
                    from_left = True
            elif (i+1, j) in neighbours: # 'F' or 'L'
                if (i,j-1) in neighbours: # 'L'
                    if from_left: # the loop came from the left
                        inside = not inside
                else: # 'F'
                    from_left = False
            if inside:
                # how many cells in this column before next loop cell?
                in_loop += j2 - 1 - j
                    
    print(f"part 2: {in_loop} cells contained by the loop")
    if answer:
        if in_loop == answer:
            print("Correct!")
        else:
            print("Incorrect!")
            
    
if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
