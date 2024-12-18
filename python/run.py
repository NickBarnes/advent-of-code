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

class AoC:
    pass

if __name__ == '__main__':
    AoC = AoC()
    AoC.args = sys.argv[1:]
    AoC.testing = '-t' in AoC.args
    if AoC.testing:
        AoC.args.remove('-t')
    AoC.verbose = '-v' in AoC.args
    if AoC.verbose:
        AoC.args.remove('-v')
    if not AoC.args:
        import datetime
        AoC.today = datetime.date.today()
        if AoC.today.month != 12 or AoC.today.day > 25:
            sys.stderr.write("Not an Advent of Code date; pass YYYY/DD as arguments.\n")
            sys.exit(1)
        AoC.args = [f"{AoC.today.year:04}/{AoC.today.day:02}"]
        
    AoC.dir = os.path.dirname(os.path.realpath(__file__))
    for AoC.year_day in AoC.args:
        print("testing" if AoC.testing else "running", AoC.year_day)
        if AoC.testing:
            AoC.files = sorted(glob.glob(f"test/{AoC.year_day}*.txt"))
        else:
            AoC.files = glob.glob(f"input/{AoC.year_day}.txt")
        AoC._src = f"{AoC.dir}/{AoC.year_day}/go.py"

        # Here is the filthy compiler hack
        AoC._py = open(AoC._src).read()
        AoC._code = compile(AoC._py, AoC._src, 'exec')
        exec(AoC._code, globals())
        
        for AoC.file in AoC.files:
            print(f"results from {AoC.file}:")
            go(open(AoC.file,'r').read())
