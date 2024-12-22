def go(input):
    initial_secrets = [int (l) for l in parse.lines(input)]

    def mix(num, secret): return num ^ secret

    def prune(num): return num % 16777216

    def generate(secret):
        secret = ((secret << 6) ^ secret) & 0xff_ff_ff
        secret = ((secret >> 5) ^ secret) & 0xff_ff_Ff
        secret = ((secret << 11) ^ secret) & 0xff_ff_Ff
        return secret

    def day_batch(secret):
        secrets = [secret]
        for i in range(2000):
            secret = generate(secret)
            secrets.append(secret)
        return secrets
    
    print("part 1 (sum of 2000th secret numbers):",
          sum(day_batch(init)[-1] for init in initial_secrets))

    # returns a dict deltas -> price for the first time
    # that sequence of four price deltas is encountered during a
    # day's trading starting with the given secret number.
    def four_delta_values(secret):
        old_price = None
        record = {}
        batch = day_batch(secret)
        a,b,c,d = None,None,None,None
        def compute(secret):
            nonlocal a,b,c,d,old_price,record
            price = secret % 10
            if old_price is not None:
                delta = price - old_price
                a,b,c,d = b,c,d,delta
            if a is not None:
                key = (a,b,c,d)
                if key not in record:
                    record[key] = price
            old_price = price
        for s in day_batch(secret):
            compute(s)
        return record

    totals = Counter()
    for init in initial_secrets:
        totals.update(four_delta_values(init))

    print("part 2 (maximum total bananas from any four-delta sequence):",
          max(totals.values()))
        

