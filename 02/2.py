import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

points = {0: 1, 1: 2, 2: 3}
result_points = {"X": 0, "Y": 3, "Z": 6}

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    p = 0
    for line in lines:
        opponent, result = line.strip().split(" ")
        opponent = ord(opponent) - ord("A")

        p += result_points[result]
        if result == "X": # lose
            p += points[(opponent - 1) % 3 ] # preceding object loses
        elif result == "Y": # draw
            p += points[opponent]
        elif result == "Z": # win
            p += points[(opponent + 1) % 3 ] # following object wins

    return p


EXPECTED_TEST_RESULT = 12
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
