def is_sum(sample, val):
    for k in sample:
        if val-k in sample:
            return True
    return False

def find_sum(data, key):
    for j in range(len(data)):
        if data[j] > key:
            continue
        sum = data[j]
        for k in range(j+1, len(data)):
            sum += data[k]
            if sum == key:
                return j,k
            if sum > key:
                break

def go(input):
    data = [int(l) for l in parse.lines(input)]
    preamble = 5 if len(data) < 100 else 25
    for i in range(preamble, len(data)):
        sample = set(data[i-preamble:i])
        if not is_sum(sample, data[i]):
            break
    key = data[i]
    print(f"part 1 (first number which isn't a sum): {key}")
    j,k = find_sum(data, key)
    weakness = min(data[j:k+1])+max(data[j:k+1])
    print(f"part 2 (sum of largest and smallest in range): {weakness}")

        
        
