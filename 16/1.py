import os
import sys
import re
from cachetools import cached

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

valve_pattern = re.compile(r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z\,\s]+)")

class Valve:
    def __init__(self, valvestring):
        re_result = valve_pattern.match(valvestring)
        self.id = re_result.group(1)
        self.flow_rate = int(re_result.group(2))
        self.tunnels = re_result.group(3).split(", ")
        # print(self.id, self.flow_rate, self.tunnels)

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    valves = {}
    for line in lines:
        valve = Valve(line.strip())
        valves[valve.id] = valve

    @cached(cache={})
    def dfs(current, opened_valves, time):
        if time == 30:
            return 0

        valve = valves[current]

        pressure = 0
        # explore opening valve if it makes sense
        if current not in opened_valves and valve.flow_rate > 0:
            pressure = dfs(valve.id, opened_valves | {valve.id}, time + 1)

        for tunnel in valve.tunnels:
            pressure = max(pressure, dfs(tunnel, opened_valves, time + 1))
        
        return pressure + sum([valves[v].flow_rate for v in opened_valves])

    return dfs("AA", frozenset(), 0)


EXPECTED_TEST_RESULT = 1651
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
