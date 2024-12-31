# Extended Euclidean algorithm. Returns g,x,y such that g = gcd(a,b)
# and a*x + b*y = g

def extended_euclid(a,b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = extended_euclid(b, a % b)
        return g, y, x - y * (a // b)

# Chinese remainder theorem for a list of (divisor, remainder) pairs,
# and all divisors are pairwise co-prime. Returns (D, R), where D is
# the product of all the divisors, and R is the remainder when any
# solution S of the problem is divided by D.  ("solution" meaning S =
# r mod d for all d,r in the list).

def chinese_remainder(l):
    while len(l) >= 2:
        div1,rem1 = l.pop()
        div2,rem2 = l.pop()
        r,coef1,coef2 = extended_euclid(div1, div2)
        assert r == 1 # co-primality
        x = rem1 * coef2 * div2 + rem2 * coef1 * div1
        div = div1 * div2
        rem = x % div
        l.append((div, rem))
    return div,rem

