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

    elfs = data.split("\n\n")
    max_calories = 0
    for elf in elfs:
        cals = [int(c) for c in elf.split("\n")]
        max_calories = max(max_calories, sum(cals))

    return max_calories


EXPECTED_TEST_RESULT = 24000
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
