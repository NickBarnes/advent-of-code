from util import *

# 2019 days 2,5,7,9 all use an "Intcode" computer.

class IntCode:
    def __init__(self, code, AoC):
        self._code = {i:v for i,v in enumerate(code)}
        self._orig = self._code.copy()
        self._AoC = AoC
        self._base = 0
        self.halted = False

    def reset(self):
        self._code = self._orig.copy()
        self._base = 0
        self.halted = False

    # number of parameters and whether they are followed by a result address
    shapes = {99: (0, False), # HALT
              1:  (2, True),  # ADD
              2:  (2, True),  # MUL
              3:  (0, True),  # IN
              4:  (1, False), # OUT
              5:  (2, False), # JUMP IF TRUE
              6:  (2, False), # JUMP IF FALSE
              7:  (2, True),  # LESS THAN
              8:  (2, True),  # EQUALS
              9:  (1, False), # ADJUST RELATIVE BASE
              }

    def _fetch(self):
        res = self._code[self._ip]
        self._ip += 1
        return res

    def _read(self, addr):
        return self._code.get(addr, 0)

    def _write(self, addr, value):
        self._code[addr] = value

    def op_params(self):
        instr = self._fetch()
        op = instr % 100
        instr //= 100
        count,write = self.shapes[op]
        params = []
        for k in range(count):
            mode = instr % 10
            instr //= 10
            if mode == 0: # indirect
                params.append(self._read(self._fetch()))
            elif mode == 1: # immediate
                params.append(self._fetch())
            else:
                assert mode == 2 # relative
                params.append(self._read(self._fetch() + self._base))
        if write: # Writes to last parameter which must be indirect
            assert instr == 0 or instr == 2
            if instr == 0:
                lvalue = self._fetch()
            else:
                lvalue = self._fetch() + self._base
        else:
            assert instr == 0 # no modes left
            lvalue = None
        return op, params, lvalue
    
    def op_2(self, fun, params, lvalue):
        self._write(lvalue, fun(params))
    
    # given an iterator over inputs, return an iterator over outputs.
    def outputs(self, inputs=iter(())):
        self._ip = 0
        while True:
            op, params, lvalue = self.op_params()
            if op == 99:  # HALT
                self.halted = True
                return
            elif op == 1: # ADD
                self.op_2(sum, params, lvalue)
            elif op == 2: # MUL
                self.op_2(misc.prod, params, lvalue)
            elif op == 3: # IN
                self._write(lvalue, next(inputs))
            elif op == 4: # OUT
                yield params[0]
            elif op == 5: # JIF:
                if params[0]:
                    self._ip = params[1]
            elif op == 6: # JELSE:
                if not params[0]:
                    self._ip = params[1]
            elif op == 7: # LT
                self._write(lvalue, 1 if params[0] < params[1] else 0)
            elif op == 8: # EQ
                self._write(lvalue, 1 if params[0] == params[1] else 0)
            elif op == 9: # ADJUST RELATIVE BASE
                self._base += params[0]
    
    # run a computer until it halts, discarding any output.
    def run(self, inputs=[]):
        list(self.outputs(iter(inputs))) # discard

    def poke(self, address, value):
        self._code[address] = value
    
    def peek(self, address):
        return self._code[address]
    
    def __repr__(self):
        if len(self._code) > 10:
            return f"<{self.__class__.__name__}({len(self._code)}): {self._code[:10]}...>"
        else:
            return f"<{self.__class__.__name__}({len(self._code)}): {self._code}>"

class LazyInputs:
    def __init__(self, init):
        self._queue = deque(init)
        self._stopped = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self._queue:
            self._stopped = True
        if not self._stopped:
            return self._queue.popleft()
        raise StopIteration

    def append(self, value):
        self._queue.append(value)
            
class PrefixInputs:
    """Make an inputs iterator which produces the values from another
    iterator preceded by a single value. The preceded iterator can be
    set after the fact by setting the `.rest` member.
    """

    def __init__(self, first, rest):
        self._first = first
        self._started = False
        self._stopped = False
        self.rest = rest
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._stopped:
            raise StopIteration
        if not self._started:
            self._started = True
            return self._first
        if self.rest is not None:
            res = next(self.rest, self)
            if res != self:
                return res
        self._stopped = True
        raise StopIteration

