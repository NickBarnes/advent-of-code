import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'util'))

import walk
import file

def extrapolate(sequence):
    if len(set(sequence)) == 1:
        return sequence[0], sequence[0]
    diffs = [sequence[i+1]-sequence[i] for i in range(len(sequence)-1)]
    diffa, diffb = extrapolate(diffs)
    return sequence[0] - diffa, sequence[-1] + diffb

def go(filename):
    print(f"results from {filename}:")
    sequences = [[int(s) for s in l] for l in file.words(filename)]
    print("part 1:", sum(extrapolate(s)[1] for s in sequences))
    print("pzrt 2:", sum(extrapolate(s)[0] for s in sequences))

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
