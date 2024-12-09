def go(input):
    print("part 1 (final frequency):",
          sum(int(x) for x in re.split(r'[,\s]+',input) if x))

    seen = set()
    freq = 0
    while len(seen) < 1_000_000: # some of the test inputs don't terminate
        for x in re.split(r'[,\s]+',input):
            if not x: continue
            freq += int(x)
            if freq in seen:
                print("part 2 (first frequency seen twice):", freq)
                break
            seen.add(freq)
        else: # didn't break; repeat outer loop
            continue
        break # broke from inner loop: we are done.
    else:
        print("no part 2 result.")
