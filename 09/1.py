import os
import sys
import numpy as np
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

directions={
    "R": np.array([1, 0]),
    "L": np.array([-1, 0]),
    "U": np.array([0, -1]),
    "D": np.array([0, 1])
}



def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    head = np.array([0,0])
    tail = np.array([0,0])
    visited = {(0,0)}

    for line in lines:
        direction, steps = line.strip().split()
        for _ in range(int(steps)):
            head += directions[direction]
            d = head - tail
            if np.max(np.abs(d)) >= 2: # is more than two tiles away in any direction
                tail += np.clip(d, -1, 1)
                visited.add(tuple(tail))

    return len(visited)


EXPECTED_TEST_RESULT = 13
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
