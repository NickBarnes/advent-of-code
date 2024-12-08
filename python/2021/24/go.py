# This was solved manually with logic and inspection of the
# inputs. The solution is laid out in this initial comment. There is
# then code to check the answer.
#
# The program is 14 repeats of this sequence of 18 instructions, with
# the only variation between repeats being the input and three
# constants c1, c2, and c3.
#
#    inp w                # w = input
#    mul x 0              # x = 0
#    add x z              # x = z
#    mod x 26             # x = z mod 26; call this z0
#    div z <c1 ? 26 : 1>  # if c1: z /= 26
#    add x <c2>           # x = z0 + c2
#    eql x w              # x = (z0 + c2 == input)
#    eql x 0              # x = (z0 + c2 != input)
#    mul y 0              # y = 0
#    add y 25             # y = 25
#    mul y x              # y = 25 
#    add y 1              # y = (z0 + c2 != input) ? 26 : 1
#    mul z y              # if (z0 + c2 != input) z *= 26
#    mul y 0              # y = 0
#    add y w              # y = w
#    add y <c3>           # y = w + c3
#    mul y x              # y = (z0 + c2 != input) ? w + c3 : 0
#    add z y              # if (z0 + c2 != input) z += w + c3
#
# The effect is that the z register works as a stack, containing
# values base 26, and each repeat will pop a value from the stack if
# c1, and will push one (equal to c3 + input) if c2 + stack_top == input.
# If the input was "valid", the stack is empty at the end.
#
# Despite the "26" hint, the values placed onto the stack don't appear
# to spell out anything interesting.
#
# So this is the loop:
# 
# z = []
# for i in range(14):
#     x = z[-1] + c2[i]
#     if c1[i]:
#        z.pop()
#     if x != d[i]:
#         z.append(d[i] + c3[i])
# if not z: print("valid")
# 
#  i        0       1       2       3       4       5       6      7       8      9     10     11     12     13
# c1 = [False,  False,  False,  False,  False,   True, False,   True,  True,  True, False,  True,  True,  True]
# c2 = [   11,     13,     12,     15,     10,     -1,    14,     -8,    -7,    -8,    11,    -2,    -2,   -13]
# c3 = [    5,      5,      1,     15,      2,      2,     5,      8,    14,    12,     7,    14,    13,     6]
# c2[i] <= 8                                        x              x      x      x             x      x      x
#
# The value we push is d[i]+c3[i]. Note that all the values we can
# push are positive, non-zero, because c3[i] > 0.
#
# We pop 7 times (when c1 is True).  So for the program to find our
# input valid, we cannot push more than 7 times.
# 
# We push if the previous stack top is not equal to d[i]-c2[i]. So we
# definitely push when c2[i] > 8, which is true 7 times, when i in
# [0,1,2,3,4,6,10]. So we push on those occasions, and cannot on any
# of the others (marked with x).
#
# So, hand-running the program, on the first five iterations we push
# these values:
# 
# d[0] + 5
# d[1] + 5
# d[2] + 1
# d[3] + 15
# d[4] + 2
# 
# Then when i=5, we must pop, so the value on the stack top (d[4] + 2)
# must be equal to d[5]-c2[5] = d[5]+1. So:
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
# Now we pop on the last three repeats:
# 
# d[10] + 5 = d[11]
# d[1] + 3 = d[12]
# d[0] - 8 = d[13]
# 
# Combining those observations, we have these constraints:
# 
# d[4] + 1 = d[5]
# d[6] - 3 = d[7]
# d[3] + 8 = d[8]
# d[2] - 7 = d[9]
# d[10] + 5 = d[11]
# d[1] + 3 = d[12]
# d[0] - 8 = d[13]
# 
# Knowing that none of the digits is zero, the +-8 constraints fix:
#
# d[0] = 9 and d[13] = 1
# d[3] = 1 and d[8] = 9
# 
# then we can relabel and state the sequence of digits is as follows:
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

# This function runs the deciphered loop, to check that the given
# `digits` pass as valid.

def simplified(digits):
    c1 = [False,  False,  False,  False,  False,  True, False,  True, True, True, False,  True, True,  True]
    c2 = [11, 13, 12, 15, 10, -1, 14, -8, -7, -8, 11, -2, -2, -13]
    c3 = [ 5,  5,  1, 15,  2,  2,  5,  8, 14, 12,  7, 14, 13,   6]

    z = [0] # dummy entry for first loop
    for i in range(14):
        x = z[-1] + c2[i]
        if c1[i]:
            z.pop()
        if x != digits[i]:
            z.append(digits[i] + c3[i])
    return z[1:] # drop dummy entry

def program(input, digits):
    reg = {'w': 0,
           'x': 0,
           'y': 0,
           'z': 0,
    }

    read = 0
    for l in input:
        words = l.split()
        cmd = words[0]
        if cmd == 'inp':
            reg[words[1]] = int(digits[read])
            read += 1
        else:
            left = words[1]
            right = words[2]
            assert left in reg
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
    return reg

def compare(input, model):
    digits = [int(c) for c in str(model)]
    reg = program(input, digits)
    stack = simplified(digits)
    z,zl = reg['z'],[]
    while z:
        zl.append(str(z % 26))
        z //= 26

    print(f"Validating model {model}:")
    print(f"  Original code produces: {reg}, stack: {' '.join(zl)}")
    print(f"  Deduced algorithm produces stack {stack}")
    print(f"  {model} is", "valid" if not stack else "invalid")

def go(input):
    max_valid = 96918996924991
    min_valid = 91811241911641
    compare(parse.lines(input), max_valid)
    compare(parse.lines(input), min_valid)
    print(f"part 1 (largest valid model number): {max_valid}")
    print(f"part 2 (smallest valid model number): {min_valid}")
