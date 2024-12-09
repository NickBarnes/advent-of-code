def basic_fuel(mass):
    return mass // 3 - 2

def gross_fuel(mass):
    sum = 0
    while True:
        mass = basic_fuel(mass)
        if mass < 0:
            return sum
        sum += mass

def go(input):
    modules = [int(l) for l in parse.lines(input)]
    print("part 1 (total basic fuel required for all modules)",
          sum(basic_fuel(m) for m in modules))

    print("part 2 (total gross fuel required for all modules)",
          sum(gross_fuel(m) for m in modules))
