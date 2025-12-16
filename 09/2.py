import os
import sys
import numpy as np
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test2.txt")
inputfile = os.path.join(dirname, "input.txt")

directions={
    "R": np.array([1, 0]),
    "L": np.array([-1, 0]),
    "U": np.array([0, -1]),
    "D": np.array([0, 1])
}

KNOTS = 10

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    knots = [np.array([0,0]) for _ in range(KNOTS)]
    visited = {(0,0)}

    for line in lines:
        direction, steps = line.strip().split()
        for _ in range(int(steps)):
            knots[0] += directions[direction]
            for i in range(1, KNOTS):
                d = knots[i-1] - knots[i]
                if np.max(np.abs(d)) >= 2: # is more than two tiles away in any direction
                    knots[i] += np.clip(d, -1, 1)
            visited.add(tuple(knots[-1]))

    return len(visited)


EXPECTED_TEST_RESULT = 36
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
