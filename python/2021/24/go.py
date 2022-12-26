import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

# The program is 14 repeats of a sequence of 18 instructions, with the
# only variation being of three constants. So there are 4 * 14 = 56
# constants, of which 14 (the digits d) are under our control.
# 
# The constants c1 are effectively just True and False
# c1 = [False,  False,  False,  False,  False,  True, False,  True, True, True, False,  True, True,  True]
# 
# c2 = [11, 13, 12, 15, 10, -1, 14, -8, -7, -8, 11, -2, -2, -13]
# c3 = [ 5,  5,  1, 15,  2,  2,  5,  8, 14, 12,  7, 14, 13,   6]
# must not push when c2 <=8: x       x   x   x       x   x    x
#
# This is the loop:
# 
# z = [0]
# for i in range(14):
#     x = z[-1] + c2[i]
#     if c1[i]:
#        z.pop()
#     if x != d[i]:
#         z.append(d[i] + c3[i])
# print(z)
#
# The value we push is d[i]+c3[i]. Note that all the values we can
# push are positive, non-zero, because c3[i] > 0.
#
# We pop 7 times.
# So we cannot push more than 7 times.
# 
# We push if the previous stack top is not equal to d[i]-c2[i]. So we
# definitely push when c2[i] > 8, which is true 7 times, when i in
# [0,1,2,3,4,6,10]. So we push on those occasions, and cannot on any
# of the others (marked with x). So the values we push are as follows:
# 
# d[0] + 5
# d[1] + 5
# d[2] + 1
# d[3] + 15
# d[4] + 2
# 
# Then when i=5, we must pop, so the value on the stack top (d[4] + 2)
# must be equal to d[5]+1. So:
#
# d[4] + 1 = d[5]
#
# Then we push when i is 6, making this stack:
# 
# d[0] + 5
# d[1] + 5
# d[2] + 1
# d[3] + 15
# d[6] + 5
# 
# Then we must pop the next three times. So,
# 
# d[6] - 3 = d[7]
# d[3] + 8 = d[8]
# d[2] - 7 = d[9]
# 
# Then we push d[10] + 7, giving this stack:
# 
# d[0] + 5
# d[1] + 5
# d[10] + 7
# 
# Now we pop the last three times:
# 
# d[10] + 5 = d[11]
# d[1] + 3 = d[12]
# d[0] - 8 = d[13]
# 
# So we have these constraints:
# 
# d[4] + 1 = d[5]
# d[6] - 3 = d[7]
# d[3] + 8 = d[8]
# d[2] - 7 = d[9]
# d[10] + 5 = d[11]
# d[1] + 3 = d[12]
# d[0] - 8 = d[13]
# 
# We know that none of the digits are zero, so we have this:
# 
#  0   1   2   3   4   5   6   7   8   9  10  11  12  13
#  9,  a,  c,  1,  d,d+1,  e,e-3,  9,c-7,  f,f+5,a+3,  1
# 
# So the largest possible solution is
# 
#  9,  6,  9,  1,  8,  9,  9,  6,  9,  2,  4,  9,  9,  1
# 
# and the smallest possible solution is
# 
#  9,  1   8,  1,  1,  2,  4,  1,  9,  1,  1,  6,  4,  1

def simplified(digits):
    c1 = [False,  False,  False,  False,  False,  True, False,  True, True, True, False,  True, True,  True]
    c2 = [11, 13, 12, 15, 10, -1, 14, -8, -7, -8, 11, -2, -2, -13]
    c3 = [ 5,  5,  1, 15,  2,  2,  5,  8, 14, 12,  7, 14, 13,   6]
    # pop when c2 <=8:         x       x   x   x       x   x    x

    z = [0]
    for i in range(14):
        x = z[-1] + c2[i]
        if c1[i]:
            z.pop()
        if x != digits[i]:
            z.append(digits[i] + c3[i])
    print(f"Model {''.join(str(d) for d in digits)}, deduced algorithm produces: {z}")

def program(filename, digits):
    lines = file.lines(filename)
    reg = {'w': 0,
           'x': 0,
           'y': 0,
           'z': 0,
    }

    read = 0

    for l in lines:
        words = l.split()
        cmd = words[0]
        if cmd == 'inp':
            reg[words[1]] = int(digits[read])
            read += 1
        else:
            left = words[1]
            right = words[2]
            right = reg[right] if right in reg else int(right)
            if cmd == 'mul':
                reg[left] *= right
            elif cmd == 'add':
                reg[left] += right
            elif cmd == 'mod':
                reg[left] %= right
            elif cmd == 'div':
                reg[left] //= right
            elif cmd == 'eql':
                reg[left] = (reg[left] == right)
    print(f"Model {''.join(str(d) for d in digits)}, original code produces: {reg}. Stack:")
    z = reg['z']
    while z:
        print("  ", z % 26)
        z //= 26

def compare(filename, model):
    digits = [int(c) for c in str(model)]
    program(filename, digits)
    simplified(digits)

def go(filename):
    print(f"results from {filename}:")

    compare(filename, 96918996924991)
    compare(filename, 91811241911641)

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
