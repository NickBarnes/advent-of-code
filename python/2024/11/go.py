def after_blinks(stones, blinks):
    stones = Counter(stones)
    for blink in range(blinks):
        new_stones = Counter()
        for stone,count in stones.items():
            if stone == 0:
                new_stones[1] += count
            else:
                s = str(stone)
                if len(s) % 2 == 0:
                    half = len(s) // 2
                    l, r = int(s[0:half]), int(s[half:])
                    new_stones[l] += count
                    new_stones[r] += count
                else:
                    new_stones[stone * 2024] += count
        stones = new_stones
    return sum(stones.values())

def go(input):
    stones = [int(w) for w in input.split() if w]
    print("part 1 (stones after 25 blinks):", after_blinks(stones, 25))
    print("part 2 (stones after 75 blinks):", after_blinks(stones, 75))
              
