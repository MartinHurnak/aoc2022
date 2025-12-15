import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

def priority(item):
        if item.islower():
            return 1 + ord(item) - ord("a")
        else:
            return 27 + ord(item) - ord("A")

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    priorities = 0
    for line in lines:
        line = line.strip()
        compartment1, compartment2 = set(line[0:len(line)//2]), set(line[len(line)//2:])
        shared = list(compartment1 & compartment2)[0]
        priorities += priority(shared)

    return priorities


EXPECTED_TEST_RESULT = 157
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
