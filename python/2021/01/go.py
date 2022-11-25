import sys

input='depths.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

depth = [int(d) for d in open(input,'r').readlines()]
answer1 = sum(1 for i in range(len(depth)-1) if depth[i] < depth[i+1])
print(f"answer 1 {answer1}")

smooth = [sum(depth[i:i+3]) for i in range(len(depth)-2)]
answer2 = sum(1 for i in range(len(smooth)-1) if smooth[i] < smooth[i+1])
print(f"answer 2 {answer2}")

