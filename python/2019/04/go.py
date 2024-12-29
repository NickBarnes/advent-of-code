def count(low, high, triples=True):
   N = 0
   # Brute force as the problem size is tiny
   for d0 in range(low // 100_000, high // 100_000+1):
       for d1 in range(d0, 10):
           for d2 in range(d1,10):
               for d3 in range(d2,10):
                   for d4 in range(d3,10):
                       for d5 in range(d4,10):
                           if d0 != d1 != d2 != d3 != d4 != d5:
                               continue
                           if not (low <=
                                   d0 * 100_000 + d1 * 10_000
                                   + d2 * 1000 + d3 * 100
                                   + d4 * 10 + d5
                                   <= high):
                               continue
                           if triples or ((d0 == d1 != d2) or
                                          (d0 != d1 == d2 != d3) or
                                          (d1 != d2 == d3 != d4) or
                                          (d2 != d3 == d4 != d5) or
                                          (d3 != d4 == d5)):
                               N += 1
   return N
 
def go(input):
    low,high = map(int, input.split('-'))
    print("part 1 (valid passwords allowing triples):",
          count(low,high))
    print("part 2 (valid passwords excluding triples):",
          count(low,high,triples=False))
