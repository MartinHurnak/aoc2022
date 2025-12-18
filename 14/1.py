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
    bounds = rocks.union(Point(500, -1)).envelope
    print(bounds)
    sands = 0 
    # slow as hell for many points
    while True:
        sand = Point(500, 0)
        settled = False
        while not settled:
            # print(sand)
            if not sand.within(bounds):
                print(sand, "out of bounds", bounds)
                return sands
            if not shapely.intersects_xy(rocks, sand.x, sand.y+1):
                sand = Point(sand.x, sand.y+1)
            elif not shapely.intersects_xy(rocks, sand.x - 1, sand.y + 1):
                sand = Point(sand.x - 1, sand.y+1)
            elif not shapely.intersects_xy(rocks, sand.x + 1, sand.y + 1):
                sand = Point(sand.x + 1, sand.y+1)
            else:
                settled = True
                
        rocks = rocks.union(sand)
        # print(rocks)
        sands += 1

    return sands


EXPECTED_TEST_RESULT = 24
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
