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
            if c == '-':   graph[(i,j)] = ((i-1,j),(i+1,j))
            elif c == '|': graph[(i,j)] = ((i,j-1),(i,j+1))
            elif c == 'F': graph[(i,j)] = ((i,j+1),(i+1,j))
            elif c == '7': graph[(i,j)] = ((i-1,j),(i,j+1))
            elif c == 'J': graph[(i,j)] = ((i-1,j),(i,j-1))
            elif c == 'L': graph[(i,j)] = ((i,j-1),(i+1,j))
            elif c == 'S':
                start=(i,j)
    # figure out graph neighbours of start point
    graph[start] = tuple(sorted(k for k in graph if start in graph[k]))
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
    print(f"part 1, max distance on loop: {d-1}")

    # part 2: how many cells contained inside loop
    # for another approach, see previous versions in git history.
    in_loop = 0
    for j in range(len(lines)):
        for i in range(len(lines[0])):
            if (i,j) not in visited:
                # shoot a ray diagonally, count times it hits the loop
                # '7' and 'L' are tangents, not hits.
                hits = 0
                for k in range(1,min(len(lines)-j, len(lines[0])-i)):
                    i2, j2 = i+k, j+k
                    if ((i2, j2) in visited
                        and graph[(i2, j2)] != ((i2, j2-1), (i2+1, j2))
                        and graph[(i2, j2)] != ((i2-1, j2), (i2, j2+1))):
                        hits += 1
                if hits % 2 == 1:
                    in_loop += 1
    print(f"part 2, cells contained: {in_loop}")
                    
    if answer:
        if in_loop == answer:
            print("Correct!")
        else:
            print("Incorrect!")
            
    
if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
