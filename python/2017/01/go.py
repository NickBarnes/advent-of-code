def go(input):
    input = input.strip()
    length = len(input)
    print("part 1 (sum of digits that match next digit):",
          sum(ord(c)-ord('0') for i,c in enumerate(input)
              if c == input[(i + 1) % length]))
    print("part 2 (sum of digits that match opposite digit):",
          sum(ord(c)-ord('0') for i,c in enumerate(input)
              if c == input[(i + length // 2) % length]))
