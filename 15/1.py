import os
import sys
import re
from shapely import GeometryCollection, Point, LineString, line_merge

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
        print(self.sensor, self.buffer)

def main(filename, y):
    with open(filename) as f:
        lines = f.readlines()

    sensors = {}
    xmin, xmax = 0, 0
    for line in lines:
        sx, sy, bx, by = tuple(int(i) for i in p.match(line.strip()).groups())
        sensors[(sx, sy)] = Sensor((sx,sy), (bx, by))
        xmin = min(xmin, sx, bx)
        xmax = max(xmax, sx, bx)
    

    line = LineString([[xmin-abs(xmin), y], [2*xmax, y]])

    collisions = GeometryCollection()
    for sensor in sensors.values():
        collision = line.intersection(sensor.buffer)
        if collision:
            collisions = line_merge(collisions.union(collision))
    
    return collisions.length


EXPECTED_TEST_RESULT = 26
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile, (10,), (2000000, ))
