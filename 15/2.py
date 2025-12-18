import os
import sys
import re
import shapely
from shapely import GeometryCollection, MultiPolygon, Point, LineString, box, line_merge

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

p = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")


class Sensor:
    def __init__(self, sensor, beacon):
        self.sensor = Point(sensor)
        self.beacon = Point(beacon)
        self.distance = abs(self.sensor.x - self.beacon.x) + abs(self.sensor.y - self.beacon.y)
        self.buffer = self.sensor.buffer(self.distance, 1)

def main(filename, xmax, ymax):
    with open(filename) as f:
        lines = f.readlines()

    sensors = []
    for line in lines:
        sx, sy, bx, by = tuple(int(i) for i in p.match(line.strip()).groups())
        sensors.append(Sensor((sx,sy), (bx, by)))
    

    map = box(0, 0, xmax, ymax)
    buffer = shapely.union_all([sensor.buffer for sensor in sensors], grid_size=1).simplify(tolerance=1)
    beacon = map.difference(buffer, grid_size=1).centroid
    return 4000000 * beacon.x + beacon.y


EXPECTED_TEST_RESULT = 56000011
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile, (20,20), (4000000, 4000000))
