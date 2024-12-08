def safe_part1(report):
    if report[1] < report[0]: # decreasing
        return safe_part1([-l for l in report])
    for i in range(len(report)-1):
        if not 1 <= report[i+1]-report[i] <= 3:
            return False
    return True
    
# It would be nice to be smarter about this, but this is easy and the
# dataset is small.

def safe_part2(report):
    return (safe_part1(report) or
            any(safe_part1(report[:i]+report[i+1:])
                for i in range(len(report))))

def go(input):
    reports = [[int(w) for w in line.split()]
               for line in parse.lines(input)]
    part1 = sum(1 for r in reports if safe_part1(r))
    print(f"part 1 (number of safe reports): {part1}")

    part2 = sum(1 for r in reports if safe_part2(r))
    print(f"part 2 (number of safe reports with problem dampener): {part2}")
        
