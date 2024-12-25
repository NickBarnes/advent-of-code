# It's Christmas, and I'm feeling playful.

def go(input):
    locks, keys = [],[] 
    for s in parse.sections(input):
        (locks if s[0][0] == '#' else keys).append(tuple(Counter(l)['#'] for l in zip(*s)))
    height = max(sum(locks,())) + 1

    print("part 1 (number of lock/key pairs):",
          sum(1
              for lock in locks
              for key in keys
              if all(h1+h2 <= height for h1,h2 in zip(lock, key))))
