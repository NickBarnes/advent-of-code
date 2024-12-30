Advent of Code

This repo has all my [Advent of Code](https://adventofcode.com/)
solutions. Advent of Code is great and everyone should give it a go.

In 2024-12 I combined Advent of Code repos from previous years into
this single repo, with a shared build/run framework and inputs
separated into a private repo as per AoC policy.

- Inputs in private repo (input/): `input/YYYY/DD.txt`
- Code in `<LANG>/<YYYY>/<DD>/` (`<LANG>` is just `python` at present).
- Test data in `test/<YYYY>/<DD>*.txt`

I haven't yet got Makefile working for this unified repo. Until I do:

    $ python3 python/run.py                     # run today's solution.
    $ python3 python/run.py YYYY/DD YYY2/D2 ... # run some solutions.
    $ make clean                                # clean up.

Pass `-t` to run with test data. It works fine with `pypy3`.

This is all BSD 2-clause licensed: feel free to steal the framework
and/or the code.

                  1111111111222222
         1234567890123456789012345
    2024 *************************
    2023 *************************
    2022 *************************
    2021 ****************     ***+
    2020 *************************
    2019 **********
    2018 **
    2017 **
    2016 **
    2015 ***
