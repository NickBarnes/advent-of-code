import math

# Extended Euclidean algorithm. Returns g,x,y such that g = gcd(a,b)
# and a*x + b*y = g

def extended_euclid(a,b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = extended_euclid(b, a % b)
        return g, y, x - y * (a // b)

# Generalised Chinese remainder theorem for a list of (divisor,
# remainder) pairs (Generalised as divisors need not be co-prime).

# Returns (D, R), where D is the lcm of all the divisors, and R is the
# remainder when any solution S of the problem is divided by D.
# ("solution" meaning S = r mod d for all d,r in the list).

def general_chinese_remainder(l):
    while len(l) >= 2:
        div1,rem1 = l.pop()
        div2,rem2 = l.pop()
        g,u,v = extended_euclid(div1, div2)
        assert rem1 % g == rem2 % g # Otherwise there are no solutions
        M = math.lcm(div1, div2)
        x = (rem1 * v * div2 + rem2 * u * div1) // g
        rem = x % M
        l.append((M, rem))
    return M,rem

