def extrapolate(sequence):
    if len(set(sequence)) == 1:
        return sequence[0], sequence[0]
    diffs = [sequence[i+1]-sequence[i] for i in range(len(sequence)-1)]
    diffa, diffb = extrapolate(diffs)
    return sequence[0] - diffa, sequence[-1] + diffb

def go(input):
    sequences = [[int(s) for s in l] for l in parse.words(input)]
    print("part 1, forwards:", sum(extrapolate(s)[1] for s in sequences))
    print("pzrt 2, back:", sum(extrapolate(s)[0] for s in sequences))
