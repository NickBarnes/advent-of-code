import random

int_re = re.compile('-?[0-9]+')

def go(input):
    lines = parse.lines(input)
    tmin, tmax = (int(x) for x in lines[0].split())
    hail = [tuple(int(x) for x in int_re.findall(line)) for line in lines[1:]]
    count = 0
    for i,(x1,y1,_,a1,b1,_) in enumerate(hail):
        for x2,y2,_,a2,b2,_ in hail[i+1:]:
            if b1/a1 == b2/a2: # lines parallel
                continue
            X = ((y2-y1)- x2*b2/a2 + x1*b1/a1)/(b1/a1-b2/a2)
            T1 = (X-x1)/a1
            T2 = (X-x2)/a2
            Y = y1+T1*b1
            if T1 < 0 or T2 < 0:
                continue
            if tmin <= X <= tmax and tmin <= Y <= tmax:
                count += 1
    print("part 1: future x/y crossings", count)

    # In vector notation:
    #
    # R + t.V = ri + t.vi
    # (R-ri) = t.(vi-V)
    # (R-ri) x (V-vi) = 0
    # R x (vi - vj) + (ri - rj) x V = ri x vi - rj x vj
    #
    # Equivalently,
    #
    # x: Y(dzi - dzj) + Z(dyj - dyi) + dY(zj - zi) + dZ(yi - yj)
    #           = yi.dzi + dyj.zj - zi.dyi - yj.dzj
    # y: Z(dxi - dxj) + X(dzj - dzi) + dZ(xj - xi) + dX(zi - zj)
    #           = zi.dxi + dzj.xj - xi.dzi - zj.dxj
    # z: X(dyi - dyj) + Y(dxj - dxi) + dX(yj - yi) + dY(xi - xj)
    #           = xi.dyi + dxj.yj - yi.dxi - xj.dyj
    #
    # These equations are linear in X,Y,Z,dX,dY,dZ. So we compute
    # these coefficients twice for distinct i,j pairs, form six
    # equations, create a matrix, and solve the set of linear
    # equations.

    hail = [(linear.Vector(x,y,z), linear.Vector(a,b,c))
            for x,y,z,a,b,c in hail]

    # Return three rows of coeffs and constants for randomly chosen hailstones.
    def equations():
        ri,dri = random.choice(hail)
        while True:
            rj,drj = random.choice(hail)
            if rj != ri or drj != dri:
                break
        xi,yi,zi = ri.v
        dxi,dyi,dzi = dri.v
        xj,yj,zj = rj.v
        dxj,dyj,dzj = drj.v

        return ([[0        , dzi - dzj, dyj - dyi, 0      , zj - zi, yi - yj],
                 [dzj - dzi, 0        , dxi - dxj, zi - zj, 0      , xj - xi],
                 [dyi - dyj, dxj - dxi, 0        , yj - yi, xi - xj, 0      ]],
                 [yi*dzi + dyj*zj - zi*dyi - yj*dzj,
                  zi*dxi + dzj*xj - xi*dzi - zj*dxj,
                  xi*dyi - yi*dxi - xj*dyj + dxj*yj])

    while True:
        rows1, es1 = equations()
        rows2, es2 = equations()
        A = linear.Matrix(rows1 + rows2)
        C = linear.matrix(es1+es2)
        d = A.determinant()
        B, d = A.inverse(divided=False)
        if B is None:
            continue
        solution = [x // d for x in (B * C).vector()]
        break

    R = linear.Vector(*(solution[i] for i in range(0,3)))
    V = linear.Vector(*(solution[i] for i in range(3,6)))
    print("part 2: sum of initial rock coordinates:", R[0] + R[1] + R[2])

    # Check
    for i,(p,v) in enumerate(hail):
        Vrel = V-v
        ts = set((p-R)[i] // Vrel[i] for i in range(3) if Vrel[i])
        assert len(ts) == 1
        t = list(ts)[0]
        collision = R + V * t
        assert collision == p + v * t

