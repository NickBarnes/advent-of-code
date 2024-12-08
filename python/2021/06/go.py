def go(input):
    ages = [int(s) for s in input.split(',')]
    agemap = {i:sum(1 for a in ages if a==i) for i in range(8)}

    def days(map,n):
        for _ in range(n):
            new = {i-1:map[i] for i in map.keys() if i > 0 and map[i] != 0}
            new[8] = map.get(0,0)
            new[6]=new.get(6,0)+map.get(0,0)
            map = new
        return map

    print(f"part 1 (after 80 days): {sum(days(agemap, 80).values())}")
    print(f"part 1 (after 256 days): {sum(days(agemap, 256).values())}")

