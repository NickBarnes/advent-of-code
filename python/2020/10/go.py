def go(input):
    jolts = sorted(int(l) for l in parse.lines(input))
    diffs = Counter(jolts[i+1]-jolts[i] for i in range(len(jolts)-1))
    diffs[jolts[0]] += 1 # from input to first adaptor
    diffs[3] += 1 # from last adaptor to device
    print("part 1 (product of 3-jolt and 1-jolt gap counts)", diffs[3] * diffs[1])

    jolts = [0] + jolts
    ways = {0: 1}
    for i in range(len(jolts)):
        adaptor = jolts[i]
        count = ways[adaptor]
        for j in range(i+1, len(jolts)):
            if jolts[j] - adaptor > 3:
                break
            ways[jolts[j]] = ways.get(jolts[j],0) + count
    print("part 2 (ways to select adaptors): ", ways[jolts[-1]])
        
