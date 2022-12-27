import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

import re

line_re = re.compile("(on|off) x=(-?[0-9]+)\.\.(-?[0-9]+),y=(-?[0-9]+)\.\.(-?[0-9]+),z=(-?[0-9]+)\.\.(-?[0-9]+)")

def reduce(orders, X1,X2,Y1,Y2,Z1,Z2):
    # reduce a set of orders to ones which apply within the X1...Z2 cuboid.
    good_orders = []
    for on,xmin,xmax,ymin,ymax,zmin,zmax in orders:
        assert xmin <= xmax
        assert ymin <= ymax
        assert zmin <= zmax
        if xmin >= X2 or xmax < X1 or ymin >= Y2 or ymax < Y1 or zmin >= Z2 or zmin < Z1:
            continue
        # intersect with initialization cuboid (also turn into base/limit pairs)
        xmin = max(X1, xmin)
        xmax = min(X2, xmax)
        ymin = max(Y1, ymin)
        ymax = min(Y2, ymax)
        zmin = max(Z1, zmin)
        zmax = min(Z2, zmax)
        good_orders.append((on,xmin,xmax,ymin,ymax,zmin,zmax))
    return good_orders

def process(orders):
    """How many cubelets remain on after processing these orders?"""

    # Partition the whole space into sub-cuboids.
    # First, find all the boundaries between sub-cuboids in each dimension
    # (note adding one to the 'max' coordinates to turn them into base/limit pairs).a
    xs = sorted(set(x for _,x1,x2,_,_,_,_ in orders for x in (x1,x2+1)))
    ys = sorted(set(y for _,_,_,y1,y2,_,_ in orders for y in (y1,y2+1)))
    zs = sorted(set(z for _,_,_,_,_,z1,z2 in orders for z in (z1,z2+1)))
    # Now quick lookups for each boundary
    xi = {x:i for i,x in enumerate(xs)}
    yi = {y:i for i,y in enumerate(ys)}
    zi = {z:i for i,z in enumerate(zs)}
    print(f"  [There are {len(xs)-1}x{len(ys)-1}x{len(zs)-1} = {(len(xs)-1)*(len(ys)-1)*(len(zs)-1)} sub-cuboids]")
    
    on_cuboids = set() # i,j,k for cuboid xs[i]-xs[i+1], ...
    flipped = 0 # interesting stat
    for on,xmin,xmax,ymin,ymax,zmin,zmax in orders:
        x1,x2 = xi[xmin],xi[xmax+1]
        y1,y2 = yi[ymin],yi[ymax+1]
        z1,z2 = zi[zmin],zi[zmax+1]
        for i in range(x1,x2):
            for j in range(y1,y2):
                for k in range(z1,z2):
                    flipped += 1
                    if on:
                        on_cuboids.add((i,j,k))
                    else:
                        on_cuboids.discard((i,j,k))
    print(f"  [{len(on_cuboids)} sub-cuboids are on, we flipped {flipped}]")

    # lookup tables for the dimensions of the sub-cuboids

    xl = {i:xs[i+1]-xs[i] for i in range(len(xs)-1)}
    yl = {i:ys[i+1]-ys[i] for i in range(len(ys)-1)}
    zl = {i:zs[i+1]-zs[i] for i in range(len(zs)-1)}

    # Surprisingly hard to add up the volumes of all the on cuboids,
    # due to out-of-memory problems (? signal 9 ?) on my MBP. The
    # obvious sum comprehension is no good. I tried various
    # workarounds, including writing everything out to file, and ended
    # up with this. Anything which iterates over the whole of
    # on_cuboids dies. Super-slow though.

    total = 0
    while on_cuboids:
        i,j,k = on_cuboids.pop()
        total += xl[i]*yl[j]*zl[k]
    return total
    
def go(filename):
    print(f"results from {filename}:")
    lines = [line_re.match(l).groups() for l in file.lines(filename)]
    orders = [(l[0] == 'on', *map(int,l[1:])) for l in lines]
    reduced = reduce(orders,-50,50,-50,50,-50,50)
    print(f"After initialization, {process(reduced)} cubes are on (answer one)")
    print(f"After full reboot, {process(orders)} cubes are on (answer two)")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
