import os
import sys
import shapely
from shapely import Point, MultiLineString
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    rocklines = []
    for line in lines:
        rocklines.append([[int(c)  for c in coords.split(",")] for coords in line.strip().split(" -> ")])
    rocks = MultiLineString(rocklines)
    max_y = rocks.bounds[-1] + 2

    sands = [Point(500, 0)]
    total_sands = 1
    for y in range(int(max_y-1)):
        new_sands = set()
        for sand in sands:
            if not shapely.intersects_xy(rocks, sand.x, sand.y+1):
                new_sands.add(Point(sand.x, sand.y+1))
            if not shapely.intersects_xy(rocks, sand.x - 1, sand.y + 1):
                new_sands.add(Point(sand.x-1, sand.y+1))
            if not shapely.intersects_xy(rocks, sand.x + 1, sand.y + 1):
                new_sands.add(Point(sand.x+1, sand.y+1))
        total_sands += len(new_sands)
        sands = new_sands

    return total_sands 

EXPECTED_TEST_RESULT = 93
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
