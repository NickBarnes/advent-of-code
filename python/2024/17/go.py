# Return outputs produced by `prog` given initial registers.

def run(prog, reg):
    def combo(ins):
        assert 0 <= ins < 7
        if ins < 4:
            return ins
        elif ins == 4:
            return reg['A']
        elif ins == 5:
            return reg['B']
        elif ins == 6:
            return reg['C']
    ip = 0
    out = []
    while ip < len(prog):
        ins = prog[ip]
        operand = prog[ip+1] if ip+1 < len(prog) else None
        if ins == 0: # adv
            reg['A'] >>= combo(operand)
        elif ins == 1: # bxl
            reg['B'] ^= operand
        elif ins == 2: # bst
            reg['B'] = combo(operand) & 7
        elif ins == 3: # jnz
            if reg['A'] != 0:
                ip = operand
                continue # don't increment ip
        elif ins == 4: # bxc
            reg['B'] ^= reg['C']
            # disregard operand
        elif ins == 5: # out
            out.append(combo(operand) & 7)
        elif ins == 6: # bdv
            reg['B'] = reg['A'] >> combo(operand)
        elif ins == 7: # cdv
            reg['C'] = reg['A'] >> combo(operand)
        ip += 2
    return out

reg_re = re.compile(r'^Register ([ABC]): ([0-9]+)$')

def go(input):
    reg_lines, prog = parse.sections(input)
    reg = {}
    for l in reg_lines:
        m = reg_re.match(l)
        assert m
        reg[m.group(1)] = int(m.group(2))

    assert len(prog) == 1
    prog = prog[0]
    assert prog.startswith('Program: ')
    prog = [int(i) for i in prog[9:].split(',')]
    
    init = reg.copy()

    print("part 1 (output of original program):",
          ','.join(str(x) for x in run(prog, reg)))

    # For part 2, we want to find a value of A which will make the
    # program produce itself. Manual analysis of the program (see
    # below) shows that it consumes A one triplet (octal digit) at a
    # time, from the low end, producing one octal digit per input
    # triplet.
    # 
    # The program performs the same operation on each triplet of A,
    # and the result depends on the low 10 bits.  So we can search,
    # one triplet at a time, finding possible leading 3k bits of A
    # which produce trailing k digits of the program.

    def recursive_trial(acc, k):
        if k == len(prog):
            return acc
        k += 1
        trials = []
        for A in acc:
            for oct in range(8):
                reg = init.copy()
                trial_A = (A << 3) + oct
                reg['A'] = trial_A
                res = run(prog, reg)
                if res == prog[-k:]:
                    trials.append(trial_A)
        if trials:
            # print(k, 'octal digits:', ' '.join('%o' % a for a in trials))
            return recursive_trial(trials, k)

    good = recursive_trial([0], 0)
    if good:
        print("part 2 (register A value to make program a Quine):",
              sorted(good)[0])
    else:
        print("part 2: no value of regster A makes program a Quine")
        
# This is the program:
#
# 2,4, 1,1, 7,5, 4,6, 0,3, 1,4, 5,5, 3,0
#
#  0: bst A
#  2: bxl 1
#  4: cdv B
#  6: bxc
#  8: adv 3
# 10: bxl 4
# 12: out B
# 14: jnz 0
#
# Happily this is a simple loop, with only one jump back to the start
# of the program.  As a Python program:
#
# while A:
#   B = A & 7
#   B = B ^ 1
#   B = B ^ (A >> B) ^ 4
#   A = A // 8
#   out.append(B & 7)
# 
# This processes A 3 bits at a time from the LSB. Each 3 bits is
# xor'ed with 1, with A shifted right by the current value, and
# finally with 4.
#
# That is:
# 
#     oct = A & 0b111
#     output (oct ^ (A >> (oct ^ 1)) ^ 0b101) & 0b111
#     A = A >> 3
#
# The hard part is the A >> (oct ^ 1). This gets three bits from a
# little higher in A (up to 7 bits higher), so can rely on the bottom
# 10 bits of A (7 + 3).

