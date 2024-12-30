def go(input):
    input = input.strip()
    assert set(input) == set('012')

    if AoC.testing:
        width,height = 2,2
    else:
        width,height = 25,6
    area = width * height
    depth = len(input) // area
    assert len(input) == area * depth

    layers = [input[area*i:area*(i+1)] for i in range(depth)]
    counters = [Counter(l) for l in layers]
    c012 = sorted((c['0'], c['1'], c['2']) for c in counters)
    least_zeroes = c012[0]
    print("part 1 (ones * twos on least-zero layer):",
          least_zeroes[1] * least_zeroes[2])

    image = []
    for pixel in zip(*layers):
        for c in pixel:
            if c == '2':
                continue
            image.append(' ' if c == '0' else '#')
            break
        else: # Shouldn't see any 'x's.
            image.append('x')

    print("part 2 (message):")
    print('\n'.join(''.join(image[j*width: (j+1)*width])
                    for j in range(height)))
