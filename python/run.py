# Simple driver script for Advent of Code programs. Invoke with some
# set of YYYY/DD arguments. If given "-t" anywhere on the command
# line, all test inputs will be run instead of the main puzzle input.
# A few useful parameters are passed to each AoC program, in an "AoC"
# object:
# 
#    AoC.testing:  a boolean: are we testing with -t?
#    AoC.verbose:  a boolean: was -v gven?
#    AoC.year_day: a string, YYYY/DD
#    AoC.file:     a string, path to the input file
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
    def __repr__(self):
        return "<AoC "+' '.join(f'{k}={v}' for k,v in self.__dict__.items())+">"

    def run():
        params = AoC()
        args = sys.argv[1:]
        params.testing = '-t' in args
        if params.testing:
            args.remove('-t')
        params.verbose = '-v' in args
        if params.verbose:
            args.remove('-v')
        if not args:
            import datetime
            today = datetime.date.today()
            if today.month != 12 or today.day > 25:
                sys.stderr.write("Today is not an Advent of Code date; pass YYYY/DD as arguments.\n")
                sys.exit(1)
            args = [f"{today.year:04}/{today.day:02}"]
            
        dir = os.path.dirname(os.path.realpath(__file__))

        path = sys.path
        success = True
        for params.year_day in args:
            src = f"{dir}/{params.year_day}/go.py"
            if not os.path.exists(src):
                sys.stderr.write(f"No solution file {src!r}.\n")
                success = False
                continue

            if params.testing:
                files = sorted(glob.glob(f"test/{params.year_day}*.txt"))
                if not files:
                    print("No test files for", params.year_day)
                    return
            else:
                files = glob.glob(f"input/{params.year_day}.txt")
            verb = "Testing" if params.testing else "Running" 
            print(f"{verb} {params.year_day}:")

            sys.path = [f"{dir}/{params.year_day}",
                        f"{dir}/{params.year_day[:4]}"] + path

            # Here is the filthy compiler hack
            py = open(src).read()
            code = compile(py, src, 'exec')
            # Tweak bindings for running AoC program.
            myglobals = globals().copy()
            # rebind "params" to "AoC".
            myglobals['AoC'] = params
            exec(code, myglobals)
            # `exec` will bind `myglobals['go']`
            if 'go' not in myglobals:
                sys.stderr.write(f"Solution file {src!r} did not define `go`.\n")
                success = False
                continue
            for params.file in files:
                print(f"results from {params.file}:")
                myglobals['go'](open(params.file,'r').read())
        if not success:
            sys.exit(1)

if __name__ == '__main__':
    # Do all the work in a function so that we don't
    # mess with the global environment.
    AoC.run()
