import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

def main(filename):
    with open(filename) as f:
        data = f.read()
    cals = [sum([int(c) for c in elf.split("\n")]) for elf in data.split("\n\n")]
    return sum(sorted(cals, reverse=True)[:3])


EXPECTED_TEST_RESULT = 45000
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
