import intcode

def go(input):
    orig = [int(s) for s in input.split(',')]
    ic = intcode.IntCode(orig, AoC)
    outputs = list(ic.outputs(inputs=[1]))
    assert all(k==0 for k in outputs[:-1])
    print("part 1 (final output after passing diagnostics):",
          outputs[-1])

    if AoC.testing and AoC.verbose:
        results = []
        tests = [0,7,8,9]
        # run test cases as provided
        for test in tests:
            ic.reset()
            results.append(list(ic.outputs(inputs=[test])))
        print(f"Testing new instructions, {tests} -> {results}")

    ic.reset()
    outputs = list(ic.outputs(inputs=[5]))
    assert len(outputs) == 1
    print("part 2 (diagnostic code):",
          outputs[0])
