from collections import deque
import os
import sys
import numpy as np
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, coords):
    for axis, size in enumerate(map.shape):
        if coords[axis] < 0 or coords[axis] >= size:
            return False
    return True

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    x_max, y_max, z_max = 0, 0, 0
    cubes_coords = set()
    for line in lines:
        cube = tuple(np.int64(c) + 1 for c in line.strip().split(",")) # offset all cubes by 1 to give enough padding if lavas would go to side
        cubes_coords.add(cube)
        x_max = max(x_max, cube[0])
        y_max = max(y_max, cube[1])
        z_max = max(z_max, cube[2])


    cubes = np.ones((x_max + 1, y_max + 1, z_max + 1))

    # BFS from outside of lava, to find the exterior
    steps = [np.array(d) for d in [[0, 0, -1], [0, 0, 1], [0, -1, 0], [0, 1, 0], [-1, 0, 0], [1, 0, 0]]]
    queue = deque()
    queue.append(np.array([0, 0, 0]))
    while queue:
        curr = queue.popleft()
        for d in steps:
            new = curr + d
            if in_map(cubes, new) and tuple(new) not in cubes_coords and cubes[tuple(new)]:
                cubes[tuple(new)] = 0
                queue.append(new)
    
    # count surfaces
    surfaces = 0
    for axis in range(3):
        surfaces += np.sum(np.abs(np.diff(cubes, axis=axis, append=0, prepend=0)))
        
    return surfaces


EXPECTED_TEST_RESULT = 58
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
