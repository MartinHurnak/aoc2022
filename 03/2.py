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

    lines = [l.strip() for l in lines]

    priorities = 0
    for elf1, elf2, elf3 in zip(lines[0::3], lines[1::3], lines[2::3]):
        badge = list(set(elf1) & set(elf2) & set(elf3))[0]
        priorities+= priority(badge)

    return priorities

EXPECTED_TEST_RESULT = 70
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
