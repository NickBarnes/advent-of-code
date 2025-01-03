def go(input):
    initial = tuple(int(c) for c in input.strip())
    state = initial
    offset = int(input[:7])
    N = len(state)

    # Let's do it with a boring matrix multiplication.
    matrix = []
    base_pattern = (0,1,0,-1)
    for i in range(N):
        row = [v for b in base_pattern for v in [b]*(i+1)]
        if len(row) < N+1:
            row *=  (N+1)//len(row)+1
        row = row[1:N+1]
        assert len(row) == N
        matrix.append(row)

    # Could speed this up by using the form of the matrix.
    def mul(vec):
        return [abs(sum(vec[j]*matrix[i][j] for j in range(N))) % 10
                for i in range(N)]

    for i in range(100):
        state = mul(state)
    print("part 1 (first 8 digits after 100 FFTs):",
          ''.join(str(v) for v in state[:8]))

    # For part 2 we have to go a *lot* faster.
    #
    # Note that the FFT patterns are complex in the early rows but
    # become 0, 0, 0, 0, ... 1, 1, 1, 1, ... once we get to N/2.
    # 
    # So for k >= N/2, the k'th digit at step i is simply the sum of
    # the k...N'th digits at step i-1. So if our offset is huge, we
    # only have to do these sums, which we can do with an accumulator
    # so each step is O(N).

    assert offset > N * 5000
    if offset > N * 10000:
        print("No part 2 for this test")
        return

    # probably a quicker way of doing this, as offset is large.
    state = list(initial*10000)[offset:]
    N = len(state)
    for i in range(100):
        acc = 0
        for j in range(-1,-N-1,-1):
            acc += state[j]
            state[j] = acc % 10
    print("part 2 (offset 8 digits after 100 expanded FFTs):",
          ''.join(str(v) for v in state[:8]))

        
        
            
    

