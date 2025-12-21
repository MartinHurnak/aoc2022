import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

def mann_dist(cube1, cube2):
    return sum(abs(c1 - c2) for c1, c2 in zip(cube1, cube2))

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    cubes = []
    sides = 0
    for line in lines:
        cube = tuple(int(c) for c in line.strip().split(","))
        sides += 6
        for other_cubes in cubes:
            if mann_dist(cube, other_cubes) <= 1:
                sides -= 2
        
        cubes.append(cube)

    return sides


EXPECTED_TEST_RESULT = 64
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
