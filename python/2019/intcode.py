# 2019 day 2 hints that we'll need quite a sophisticated "Intcode"
# computer implementation, so I've moved it out here where the code
# can be shared.

def run(code):
    ip = 0
    while True:
        if code[ip] == 99:  # HALT
            return
        elif code[ip] == 1: # ADD
            code[code[ip+3]] = code[code[ip+1]] + code[code[ip+2]]
            ip += 4
        elif code[ip] == 2: # MUL
            code[code[ip+3]] = code[code[ip+1]] * code[code[ip+2]]
            ip += 4
