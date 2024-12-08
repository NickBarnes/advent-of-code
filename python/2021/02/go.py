import sys

input='course.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

course = [(s[0], int(s[1])) for l in open(input,'r').readlines() if (s := l.split())]
tf = sum(n for (d,n) in course if d == 'forward')
td = sum(n for (d,n) in course if d == 'down')
tu = sum(n for (d,n) in course if d == 'up')
depth = td-tu
product = tf * depth
print(f"total forward {tf}, total depth {depth}, answer 1 {product}")

h = 0
aim = 0
d = 0
for (direction, distance) in course:
    if direction == 'down':
        aim += distance
    elif direction == 'up':
        aim -= distance
    elif direction == 'forward':
        h += distance
        d += distance * aim
product = h * d
print(f"distance {h} depth {d} answer 2 {product}")

        

