def part1_ops(acc, inp):
    return (acc + inp, acc * inp)

# Offensive implementation, but this nicer one is no faster
# mul,div = 10, inp
# while div > 10:
#     mul, div = mul * 10, div // 10
# return (acc + inp, acc * inp, acc * mul + inp)

def part2_ops(acc, inp):
    return (acc + inp, acc * inp, int(str(acc)+str(inp)))

def go(input):
    equations = []
    for line in parse.lines(input):
        result, inputs = line.split(':')
        result = int(result)
        inputs = [int(i) for i in inputs.split()]
        equations.append((result, inputs))

    def matches(ops):
        good = 0
        for res, inputs in equations:
            partials = {inputs[0]}
            for input in inputs[1:]:
                partials = set(r for p in partials for r in ops(p, input))
            if res in partials:
                good += res
        return good

    print("part 1 (with addition and multiplication):", matches(part1_ops))
    print("part 2 (with addition, multiplication, and concatenation)", matches(part2_ops))
