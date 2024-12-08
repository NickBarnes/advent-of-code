def go(input):
    depth = [int(d) for d in parse.lines(input)]

    answer1 = sum(1 for i in range(len(depth)-1) if depth[i] < depth[i+1])
    print(f"part 1 (depth increases): {answer1}")

    smooth = [sum(depth[i:i+3]) for i in range(len(depth)-2)]
    answer2 = sum(1 for i in range(len(smooth)-1) if smooth[i] < smooth[i+1])
    print(f"part 2 (smoothed depth increases): {answer2}")

