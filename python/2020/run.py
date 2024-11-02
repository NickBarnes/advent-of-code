from util import *
import sys
import glob
import os

if __name__ == '__main__':
    testing = '-t' in sys.argv[1:]
    for d in sys.argv[1:]:
        if d == '-t':
            continue
        
        if testing:
            files = sorted(glob.glob(f"{d}/test*.txt"))
        else:
            files = glob.glob(f"{d}/input.txt")
        src = f"{d}/go.py"
        py = open(src).read()
        code = compile(py, src, 'exec')
        exec(code, globals())
        
        for file in files:
            print(f"results from {file}:")
            go(open(file,'r').read())
