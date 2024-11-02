insn_re = re.compile('^(acc|nop|jmp) ([+-][0-9]+)$')
# util/__init__.py.

def run(code, pc=1, acc=0, visited=set(), flex=False):
    visited = visited.copy()
    while pc not in visited:
        if pc == len(code)+1:
            return "terminated", acc
        elif pc <= 0 or pc > len(code)+1:
            return f"jumped to {pc}", acc

        visited.add(pc)
        op, imm = code[pc-1]
        if op == 'jmp':
            if flex: # try change jmp to nop
                alt = run(code, pc+1, acc, visited, False)
                if alt[0] == 'terminated':
                    return f"change {pc} from jmp to nop", alt[1]
            pc += imm
        elif op == 'acc':
            acc += imm
            pc += 1
        else: # nop
            if flex: # try change nop to jmp
                alt = run(code, pc+imm, acc, visited, False)
                if alt[0] == 'terminated':
                    return f"change {pc} from nop to jmp", alt[1]
            pc += 1 # just a nop
                
    return f"looped at {pc}", acc


def go(input):
    code = [(m.group(1), int(m.group(2))) for l in parse.lines(input) if (m := insn_re.match(l))]
    terminate, acc = run(code, flex=False)
    print(f"part 1 (without changes) {terminate}: {acc}")

    terminate, acc = run(code, flex=True)
    print(f"part 2 (with a change) {terminate}: {acc}")
