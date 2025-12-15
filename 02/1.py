import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

beats = {
    "X": "C",
    "Y": "A",
    "Z": "B",
}

points = {"X":1, "Y": 2, "Z": 3}

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    p = 0
    for line in lines:
        opponent, me = line.strip().split(" ")
        p += points[me]
        if beats[me] == opponent:
            p += 6
        elif ord(me) - ord("X") == ord(opponent) - ord("A"):
            p += 3

    return p


EXPECTED_TEST_RESULT = 15
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
