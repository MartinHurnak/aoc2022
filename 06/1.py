import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

MARKER_LEN = 4 

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    signal = lines[0].strip()
    for i in range(MARKER_LEN, len(signal)):
        if len(set(signal[i-MARKER_LEN:i])) == MARKER_LEN:
            return i

EXPECTED_TEST_RESULT = 7
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
