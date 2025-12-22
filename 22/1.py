import os
import sys
import re
import numpy as np
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

def rotate_clockwise(orientation):
    return np.flip(orientation) * np.array([-1, 1])

def rotate_counterclockwise(orientation):
    return np.flip(orientation) * np.array([1, -1])

class MapRow:
    def __init__(self, row):
        self.start = len(row) - len(row.lstrip()) 
        self.end = len(row.rstrip()) - 1
        self.walls = [i for i,c in enumerate(row) if row[i] == "#"]

    def __repr__(self):
        return str((self.start, self.end, self.walls))

    def is_wall(self, x):
        return x in self.walls
    
    def is_inside(self, x):
        return self.start <= x <= self.end
    
    def wrap_horizontally(self, x):
        if x < self.start:
            return self.end - (self.start - x - 1)
        elif x > self.end:
            return self.start + (x - self.end - 1) 
        else:
            return x

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    path = lines[-1].strip()
    map = [MapRow(line) for line in lines[:-1]]

    position = np.array([min(i for i in range(map[0].start, map[0].end) if i not in map[0].walls), 0])
    orientation = np.array([1, 0])

    pattern = re.compile(r"(\d+|[RL])")
    for instruction in pattern.findall(path):
        try:
            steps = int(instruction)
            for _ in range(steps):
                new_pos = position + orientation
                if map[new_pos[1]].is_wall(new_pos[0]):
                    break
                if not map[new_pos[1]].is_inside(new_pos[0]):
                    if orientation[0] != 0:
                        new_pos[0] = map[new_pos[1]].wrap_horizontally(new_pos[0])
                        # print(position, "wrap horizontally to", new_pos)
                    
                    if orientation[1] != 0:
                        y_wrap = new_pos[1] 
                        while 0 <= y_wrap - orientation[1] < len(map) and map[y_wrap - orientation[1]].is_inside(new_pos[0]):
                            y_wrap += -orientation[1]
                        if not map[y_wrap].is_wall(new_pos[0]):
                            new_pos[1] = y_wrap
                            # print(position, "wrap vertically to", new_pos, orientation)
                        else:
                            new_pos[1] -= orientation[1] # unsuccessful wrap, step back
                            # print(position, "wrap hit the wall, ignored wrap at", new_pos)
                            break
                position = new_pos
        except ValueError:
            if instruction == "R":
                orientation = rotate_clockwise(orientation)
            else:
                orientation = rotate_counterclockwise(orientation)

    orientation_code ={
        (1, 0): 0,
        (0, 1): 1,
        (-1, 0): 2,
        (0, -1): 3
    }[tuple(orientation)]
    return 1000 * (position[1] + 1) + 4* (position[0] + 1) + orientation_code


EXPECTED_TEST_RESULT = 6032
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
