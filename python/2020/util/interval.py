# Integer interval arithmetic. Comes up surprisingly often.

import functools

# A single interval.

@functools.total_ordering
class Interval:
    def __init__(self, base, limit):
        self.base = base
        self.limit = limit

    def __repr__(self):
        return f"[{self.base}, {self.limit})"

    def __len__(self):
        return self.limit-self.base

    def __eq__(self, other):
        return (self.base == other.base) and (self.limit == other.limit)

    def __lt__(self, other):
        return ((self.base, self.limit) < (other.base, other.limit))

    # intersection - may be None
    def __and__(self, other):
        if self.base <= other.limit and other.base <= self.limit:
            # overlapping
            return Interval(max(self.base, other.base),
                            min(self.limit, other.limit))

    # union - may be several Intervals, yielded in order
    def __or__(self, other):
        if self.base > other.limit or other.base > self.limit:
            if self < other:
                yield self
                yield other
            else:
                yield other
                yield self
        else:
            # overlapping
            yield Interval(min(self.base, other.base),
                           max(self.limit, other.limit))

    # difference (asymmetric). May be several intervals, yielded in order,
    # or none.
    def __sub__(self, other):
        if self.base > other.limit or other.base > self.limit:
            yield self
        else: # overlapping
            if self.base < other.base:
                yield Interval (self.base, other.base)
            if self.limit > other.limit:
                yield Interval (other.limit, self.limit)

    def __contains__(self,i):
        return self.base <= i < self.limit

    def __bool__(self):
        return self.base < self.limit

    # same interval, offset by some constant
    def offset(self, k):
        return Interval(self.base+k, self.limit+k)

# A set of integer intervals, kept normalised (i.e. non-overlapping,
# in increasing order).

class Intervals:

    # initialize with either an iterable of Interval objects (which
    # should be in order) or an iterable of (base, limit) pairs (which
    # will be normalised).
    def __init__(self, l):
        if not l:
            self.ints = []
        elif isinstance(l[0], Interval):
            self.ints = l.copy()
        else: # normalise
            l = sorted(l)
            assert all(len(i) == 2 for i in l)
            assert all(i[0] < i[1] for i in l)
            i = 0
            self.ints = []
            while i < len(l):
                base = l[i][0]
                limit = l[i][1]
                i = i+1
                while i < len(l) and limit >= l[i][0]:
                    # merge
                    limit = max(limit, l[i][1])
                    i = i+1
                self.ints.append(Interval(base,limit))

    def count(self):
        return len(self.ints)
    
    def __repr__(self):
        return (f"<{len(self.ints)}:" + (", ".join(repr(i) for i in self.ints))
                + f" ({len(self)})>")

    def __len__(self):
        return sum(len(i) for i in self.ints)

    # difference: remove one interval at a time.
    def __sub__(self, other):
        ints = self.ints
        for i2 in other.ints:
            ints = [j for i in ints for j in i - i2]
        return Intervals(ints)

    # intersection - we renormalise
    def __and__(self, other):
        return Intervals([(x.base,x.limit)
                          for i in self.ints
                          for o in other.ints
                          if (x := i & o)])

    # union - just use the normaliser
    def __or__(self, other):
        return Intervals([(x.base, x.limit) for l in (self.ints, other.ints)
                          for x in l])

    def __contains__(self,i):
        return any(i in inter for inter in self.ints)

    def __bool__(self):
        return any(i for i in self.ints)

    
        
