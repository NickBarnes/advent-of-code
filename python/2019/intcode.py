from util import *

# 2019 day 2 hints that we'll need quite a sophisticated "Intcode"
# computer implementation, so I've moved it out here where the code
# can be shared.

class IntCode:
    def __init__(self, code, AoC):
        self._code = code.copy()
        self._orig = code.copy()
        self._AoC = AoC

    def reset(self):
        self._code = self._orig.copy()

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
              }

    def op_params(self):
        instr = self._code[self._ip]
        self._ip += 1
        op = instr % 100
        instr //= 100
        count,write = self.shapes[op]
        params = []
        for k in range(count):
            mode = instr % 10
            instr //= 10
            if mode == 1: # immediate
                params.append(self._code[self._ip])
            else: # indirect
                params.append(self._code[self._code[self._ip]])
            self._ip += 1
        assert instr == 0 # no modes left
        lvalue = None
        if write: # Writes to last parameter which must be indirect
            lvalue = self._code[self._ip]
            self._ip += 1
        return op, params, lvalue
    
    def op_2(self, fun, params, lvalue):
        self._code[lvalue] = fun(params)
    
    def outputs(self, inputs=[]):
        self._ip = 0
        inputs = deque(inputs)
        while True:
            op, params, lvalue = self.op_params()
            if op == 99:  # HALT
                return
            elif op == 1: # ADD
                self.op_2(sum, params, lvalue)
            elif op == 2: # MUL
                self.op_2(misc.prod, params, lvalue)
            elif op == 3: # IN
                self._code[lvalue] = inputs.popleft()
            elif op == 4: # OUT
                yield params[0]
            elif op == 5: # JIF:
                if params[0]:
                    self._ip = params[1]
            elif op == 6: # JELSE:
                if not params[0]:
                    self._ip = params[1]
            elif op == 7: # LT
                self._code[lvalue] = 1 if params[0] < params[1] else 0
            elif op == 8: # EQ
                self._code[lvalue] = 1 if params[0] == params[1] else 0
    
    def run(self, inputs=[]):
        list(self.outputs(inputs))

    def poke(self, address, value):
        self._code[address] = value
    
    def peek(self, address):
        return self._code[address]
    
    def __repr__(self):
        if len(self._code) > 10:
            return f"<{self.__class__.__name__}({len(self._code)}): {self._code[:10]}...>"
        else:
            return f"<{self.__class__.__name__}({len(self._code)}): {self._code}>"
