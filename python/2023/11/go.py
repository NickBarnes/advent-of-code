import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))
import walk
import file
import interval
import misc

def expand(galaxies, empty_rows, empty_cols, factor):
    return list((i + di*(factor-1), j + dj*(factor-1))
                for (i,j) in galaxies
                if ((di := sum(1 for ei in empty_cols if ei < i)) > -1
                    and (dj := sum(1 for ej in empty_rows if ej < j)) > -1))

def total_distance(galaxies):
    return sum(abs(galaxies[l][0]-galaxies[k][0]) +
               abs(galaxies[l][1]-galaxies[k][1])
               for k in range(len(galaxies))
               for l in range(k))

def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)
    galaxies = set((i,j) for j in range(len(lines))
                   for i in range(len(lines[j]))
                   if lines[j][i] == '#')
    rows = set(j for (i,j) in galaxies)
    cols = set(i for (i,j) in galaxies)
    empty_rows = set(j for j in range(len(lines)) if j not in rows)
    empty_cols = set(i for i in range(len(lines[0])) if i not in cols)
    
    print(f"part 1, total distance with expansion 2:",
          total_distance(expand(galaxies, empty_rows, empty_cols, 2)))
    print(f"part 2, total distance with expansion 1000000:",
          total_distance(expand(galaxies, empty_rows, empty_cols, 1000000)))

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
