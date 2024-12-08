import sys
import functools

# Python made this one really easy with bignums

class Bits:
    def __init__(self, s):
        s = s.strip()
        self._v = int(s, base=16) # bignum
        self._n = len(s) * 4 # how many live bits

    def get(self, n):
        res = self._v >> (self._n - n)
        self._v &= ((1 << (self._n - n))-1)
        self._n -= n
        return res

    def n(self):
        return self._n

# Construct recursively

class Packet:
    def __init__(self,s=None, b=None):
        if s:
            self._bits = Bits(s)
        else:
            self._bits = b
        start_n = self._bits.n()
        self._version = self._bits.get(3)
        self._type_id = self._bits.get(3)
        self._literal = None
        self._packets = []
        if self._type_id == 4:
            self._set_literal()
        else:
            self._set_operator()
        self._len = start_n - self._bits.n()

    def len(self):
        return self._len

    def literal(self):
        return self._literal

    def value(self):
        if self._type_id == 4:
            return self._literal
        elif self._type_id == 0:
            return sum(p.value() for p in self._packets)
        elif self._type_id == 1:
            return functools.reduce(lambda x,y: x * y, (p.value() for p in self._packets), 1)
        elif self._type_id == 2:
            return min(p.value() for p in self._packets)
        elif self._type_id == 3:
            return max(p.value() for p in self._packets)
        elif self._type_id == 5:
            return 1 if self._packets[0].value() > self._packets[1].value() else 0
        elif self._type_id == 6:
            return 1 if self._packets[0].value() < self._packets[1].value() else 0
        elif self._type_id == 7:
            return 1 if self._packets[0].value() == self._packets[1].value() else 0

    def sub_packets(self):
        return self._packets

    def total_versions(self):
        return self._version + sum(p.total_versions() for p in self._packets)

    def _set_literal(self):
        l = 0
        while True:
            nibble = self._bits.get(5)
            l = (l << 4) + (nibble & 15)
            if (nibble & 16) == 0:
                break
        self._literal = l

    def _set_operator(self):
        length_type = self._bits.get(1)
        if length_type == 1:
            packets = self._bits.get(11)
            while packets:
                self._packets.append(Packet(b=self._bits))
                packets -= 1
        else: # length type 0: bit count
            bits = self._bits.get(15)
            while bits:
                packet = Packet(b=self._bits)
                self._packets.append(packet)
                bits -= packet.len()

def go(input):
    for l in parse.lines(input):
        packet = Packet(s=l)
        print(f"part 1 (total packet versions): {packet.total_versions()}")
        print(f"part 2 (expression value): {packet.value()}")
