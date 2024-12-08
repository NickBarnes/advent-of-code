# Simple driver script for Advent of Code instances. Invoke with some
# set of YYYY/DD arguments. If given "-t" anywhere on the command
# line, all test inputs will be run instead of the main puzzle input.
# 
# Should be run from the top directory in the repo, where
# sub-directories test/ and input/ contain test and input files
# respectively. 
#
# If invoked on an AoC date, without any YYYY/DD arguments, will
# attempt to run today's solution.
#
# This script uses a filthy Python compiler hack, and would definitely
# be easy to destroy by giving it a suitable puzzle solution.

import sys
import glob
import os

from util import *

if __name__ == '__main__':
    args = sys.argv[1:]
    testing = '-t' in args
    if testing:
        args.remove('-t')
    if not args:
        import datetime
        today = datetime.date.today()
        if today.month != 12 or today.day > 25:
            sys.stderr.write("Not an Advent of Code date; pass YYYY/DD as arguments.\n")
            sys.exit(1)
        args = [f"{today.year:04}/{today.day:02}"]
        
    dir = os.path.dirname(os.path.realpath(__file__))
    for year_day in args:
        print("testing" if testing else "running", year_day)
        if testing:
            files = sorted(glob.glob(f"test/{year_day}*.txt"))
        else:
            files = glob.glob(f"input/{year_day}.txt")
        src = f"{dir}/{year_day}/go.py"

        # Here is the filthy compiler hack
        py = open(src).read()
        code = compile(py, src, 'exec')
        exec(code, globals())
        
        for file in files:
            print(f"results from {file}:")
            go(open(file,'r').read())
