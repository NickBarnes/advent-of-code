from util import *
import sys
import glob
import os

if __name__ == '__main__':
    testing = '-t' in sys.argv[1:]
    dir = os.path.dirname(os.path.realpath(__file__))
    for day in sys.argv[1:]:
        if day == '-t':
            continue
        
        if testing:
            files = sorted(glob.glob(f"{dir}/{day}/test*.txt"))
        else:
            files = glob.glob(f"input/{day}.txt")
        src = f"{dir}/{day}/go.py"
        py = open(src).read()
        code = compile(py, src, 'exec')
        exec(code, globals())
        
        for file in files:
            print(f"results from {file}:")
            go(open(file,'r').read())
