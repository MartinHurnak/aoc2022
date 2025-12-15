import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    overlaps =0
    for line in lines:
        assignments = line.strip().split(",")
        assignments = [tuple([int(i) for i in assignment.split("-")]) for assignment in assignments]
        assignment1, assignment2 = tuple(sorted(assignments))
       
        if assignment1[1] >= assignment2[0]:
            overlaps += 1

    return overlaps


EXPECTED_TEST_RESULT = 4
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
