# returns r,s,t such that r = gcd(a,b) and a*s + b*t = r

def extended_euclid(a,b):
    r,nr = a,b
    s,ns = 1,0
    t,nt = 0,1
    while nr != 0:
        q = r // nr
        r,nr = nr, r - q * nr
        s,ns = ns, s - q * ns
        t,nt = nt, t - q * nt
    return r,s,t

# Chinese remainder theorem for a list of (divisor, remainder) pairs.
# Returns (D, R), where D is the product of all the divisors, and R is
# the remainder when any solution S of the problem is divided by D.
# ("solution" meaning S = r mod d for all d,r in the list).

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

def go(input):
    lines = parse.lines(input)
    start = int(lines[0])
    buses = [(int(b), i)
             for i, b in enumerate(lines[1].split(','))
             if b != 'x']

    # part 1
    bus = sorted((b - (start % b), b) for b,_ in buses)[0]
    print("part 1 (product of bus# and wait):", bus[0]*bus[1])

    # part 2
    remainders = [(b, b-i) for b,i in buses]
    print("part 2 (timestamp of desired bus arrival pattern)", chinese_remainder(remainders)[1])

    
    
