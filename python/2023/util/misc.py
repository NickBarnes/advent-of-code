import functools

def prod(iterable):
    return functools.reduce(lambda a,b: a*b, iterable)
