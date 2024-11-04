# We define a "parse tree" as either `('int', i)` for some integer `i`
# or ('list', [t0, (op1, t1), (op2, t2), ...]) for sub-trees ti and
# operators opi (operators being '*' or '+').

def parse_val(s,i):
    """Return the parse tree of the value starting at position `i` in `s`,
    and the position following the last character of that value."""
    
    if s[i] == '(':
        return parse_tree(s,i+1)
    j = i
    while(j < len(s) and s[j].isdigit()):
        j += 1
    assert j != i
    return ('int', int(s[i:j])), j

def parse_tree(s, i=0):
    """Return the parse tree of the infix expression (of the general
    form "e0 op1 e1 op2 e2 ... en" starting at position `i` in `s`,
    and the position following the last character of that expression.
    """
    val, i = parse_val(s,i)
    l = [val]
    while i < len(s) and s[i] != ')':
        assert s[i] == ' '
        assert len(s) >= i+4
        op = s[i+1]
        assert op in '+*'
        assert s[i+2] == ' '
        val2, i = parse_val(s,i+3)
        l.append((op, val2))
    if i < len(s):
        assert s[i] == ')'
        i += 1
    return ('list',l), i

def eval_tree_part1(t):
    """Return the value of the parse tree `t` according to the rules
    of part 1 (evaluating operators in left-to-right order)."""
    if t[0] == 'int':
        return t[1]
    elif t[0] == 'list':
        v = eval_tree_part1(t[1][0])
        for op,sub in t[1][1:]:
            v2 = eval_tree_part1(sub)
            v = v * v2 if op == '*' else v + v2
        return v
    else:
        assert False

def eval_tree_part2(t):
    """Return the value of the parse tree `t` according to the rules
    of part 2 (addition takes precedence over multiplication)."""
    if t[0] == 'int':
        return t[1]
    elif t[0] == 'list':
        # An infix expression is some number of "factors", each of
        # which is a sum t1 + ... + tn. Compute each factor as we go
        # along, and multiply when each one is complete.
        acc = 1
        v = eval_tree_part2(t[1][0])
        rest = []
        for op,sub in t[1][1:]:
            v2 = eval_tree_part2(sub)
            if op == '+': # do additions immediately.
                v += v2
            else:
                assert op == '*'
                # We've reached the end of this factor.
                acc *= v
                v = v2
        return acc * v
    else:
        assert False

def go(input):
    print(sum(eval_tree_part1(t) for line in parse.lines(input) if (t := parse_tree(line)[0])))
    print(sum(eval_tree_part2(t) for line in parse.lines(input) if (t := parse_tree(line)[0])))
