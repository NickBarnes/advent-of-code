def least_heat(digits, ultra=False, debug=False):
    rows = len(digits)
    cols = len(digits[0])
    max_run = 10 if ultra else 3
    min_run = 4 if ultra else 1
    def weights(n):
        i,j,di,dj,c = n
        ds = []
        results = []
        def dir(ndi,ndj):
            ni,nj = i+ndi, j+ndj
            if 0 <= ni < cols and 0 <= nj < rows:
                results.append(((ni,nj,ndi,ndj, c+1 if di == ndi and dj == ndj else 1),
                                digits[nj][ni]))
        if di:
            if c == 0 or c >= min_run: # can turn
                dir(0,1)
                dir(0,-1)
            if c != max_run: # can continue
                dir(di,0)
        if dj:
            if c == 0 or c >= min_run: # can turn
                dir(1,0)
                dir(-1,0)
            if c != max_run: # can continue
                dir(0,dj)
        return results
    shortest = graph.shortest_tree((0,0,1,0,0), weights)
    return min(w for n,w in shortest.items()
               if n[0] == cols-1 and n[1] == rows-1
               and ((not ultra) or (n[4] >= min_run)))

def go(input):
    digits = parse.digits(input)
    print("part 1, least heat with regular crucibles:", least_heat(digits))
    print("part 2, least heat with ultra crucibles:",
          least_heat(digits, ultra = True))
