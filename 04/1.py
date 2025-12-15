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

    full_overlaps =0
    for line in lines:
        assignments = line.strip().split(",")
        assignments = [tuple([int(i) for i in assignment.split("-")]) for assignment in assignments]
        assignment1, assignment2 = tuple(assignments)
       

        if assignment1[0] <= assignment2[0] and assignment2[1] <= assignment1[1]:
            full_overlaps += 1
        elif assignment2[0] <= assignment1[0] and assignment1[1] <= assignment2[1]:
            full_overlaps += 1

    return full_overlaps


EXPECTED_TEST_RESULT = 2  
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
