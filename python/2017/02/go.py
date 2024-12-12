def go(input):
    sheet = [[int(w) for w in l] for l in parse.words(input)]
    print("part 1 (spreadsheet checksum):",
          sum(max(l)-min(l) for l in sheet))

    total = 0
    for l in sheet:
        for a in l:
            mults = [b for b in l if b > a and b % a == 0]
            if mults:
                assert len(mults) == 1
                total += mults[0] // a
                break
    print("part 2 (total of quotients):", total)
                
