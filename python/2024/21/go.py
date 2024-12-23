numeric_pad = intgrid.IntGrid(['789','456','123',' 0A'], ignore=' ')

directional_pad = intgrid.IntGrid([' ^A','<v>'], ignore = ' ')

memo = {}
# Find the shortest sequence of moves to get from 'start' to 'end' on
# 'pad' without crossing the gap. The sequences generated are
# preferentially repetitious.
def key_routes(pad, start, end):
    k = (pad, start, end)
    if k in memo:
        return memo[k]
    p = pad.find_only(start)
    end = pad.find_only(end)
    horiz = abs(p.x - end.x) * ('<' if p.x > end.x else '>')
    vert = abs(p.y - end.y) * ('^' if p.y > end.y else 'v')
    routes = []
    if pad.get(intgrid.V2(p.x, end.y)) is not None:
        routes.append(vert + horiz + 'A')
    if pad.get(intgrid.V2(end.x, p.y)) is not None:
        routes.append(horiz + vert + 'A')
    memo[k] = routes
    return routes

cache = {}
# Find the minimum length of input to produce `code` at level `level`
# in a sequence of `pads`.
def min_len(code, pads, level):
    k = (code, level)
    if k in cache:
        return cache[k]
    if level == 0:
        res = len(code)
    else:
        level -= 1
        s = 'A'+code
        res = sum(min(min_len(k, pads, level)
                      for k in key_routes(pads[level], s[i], s[i+1]))
                  for i in range(len(s)-1))
    cache[k] = res
    return res

def complexity(robots, codes):
    cache = {}
    pads = [directional_pad] * (robots-1) + [numeric_pad]
    return sum(min_len(code, pads, len(pads)) * int(code[:-1])
               for code in codes)
    

def go(input):
    global numeric_pad, directional_pad, route
    codes = parse.lines(input)
    print("part 1 (total complexity with 2 directional pads):",
          complexity(3, codes))

    cache = {}
    pads = [directional_pad]*25 + [numeric_pad]
    print("part 2 (total complexity with 26 directional pads):",
          complexity(26, codes))
