import os
import sys
import re
import copy
from cachetools import cachedmethod
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

pattern = re.compile(r"Blueprint (\d+):\s*Each ore robot costs (\d+) ore.\s*Each clay robot costs (\d+) ore.\s*Each obsidian robot costs (\d+) ore and (\d+) clay.\s*Each geode robot costs (\d+) ore and (\d+) obsidian.")

class RobotsAndResources:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0
    
        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0
    
    def mine(self):
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geode += self.geode_robots
        return self

    def build_ore_robot(self):
        new = copy.copy(self)
        new.mine()
        new.ore_robots +=1
        new.ore -= self.blueprint.ore_robot_ore
        return new
    
    def build_clay_robot(self):
        new = copy.copy(self)
        new.mine()
        new.clay_robots +=1
        new.ore -= self.blueprint.clay_robot_ore
        return new

    def build_obsidian_robot(self):
        new = copy.copy(self)
        new.mine()
        new.obsidian_robots +=1
        new.ore -= self.blueprint.obsidian_robot_ore
        new.clay -= self.blueprint.obsidian_robot_clay
        return new
    
    def build_geode_robot(self):
        new = copy.copy(self)
        new.mine()
        new.geode_robots +=1
        new.ore -= self.blueprint.geode_robot_ore
        new.obsidian -= self.blueprint.geode_robot_obsidian
        return new

def cache_key(self, time, state, **kwargs):
    return (time, state.ore, state.clay, state.obsidian, state.geode, state.ore_robots, state.clay_robots, state.obsidian_robots, state.geode_robots)

class Blueprint:
    def __init__(self, id, ore_robot_ore, clay_robot_ore, obsidian_robot_ore, obsidian_robot_clay, geode_robot_ore, geode_robot_obsidian):
        self.id = id
        self.ore_robot_ore = ore_robot_ore
        self.clay_robot_ore = clay_robot_ore
        self.obsidian_robot_ore = obsidian_robot_ore
        self.geode_robot_ore = geode_robot_ore
        self.obsidian_robot_clay = obsidian_robot_clay
        self.geode_robot_obsidian = geode_robot_obsidian
        self.cache = {}
        self.max_ore_cost = max(ore_robot_ore, clay_robot_ore, obsidian_robot_ore, geode_robot_ore)


    @cachedmethod(lambda self: self.cache, key=cache_key)
    def dfs(self, time, state):
        if time == 0:
            return state.geode
        geodes = 0
        # assume we always want to build geode robot or obsidian robot, since they are quite expensive
        if state.ore >= self.geode_robot_ore and state.obsidian >= self.geode_robot_obsidian:
            return max(geodes, self.dfs(time - 1, state.build_geode_robot()))
        if state.ore >= self.obsidian_robot_ore and state.clay >= self.obsidian_robot_clay:
            return max(geodes, self.dfs(time - 1, state.build_obsidian_robot()))
        # we can build only one robot per minute, robots dont require much ore so it does not make sense to have more ore robots than most expensive
        if state.ore >= self.ore_robot_ore  and state.ore_robots < self.max_ore_cost:
            geodes = max(geodes, self.dfs(time - 1, state.build_ore_robot()))
        if state.ore >= self.clay_robot_ore:
            geodes = max(geodes, self.dfs(time - 1, state.build_clay_robot()))


        geodes = max(geodes, self.dfs(time -1, state.mine())) 

        return geodes


def main(filename):
    with open(filename) as f:
        lines = f.read()

    quality = 0
    for bp in re.findall(pattern, lines):
        blueprint = Blueprint(*tuple(int(i) for i in bp))
        geodes = blueprint.dfs(24, RobotsAndResources(blueprint))
        quality += blueprint.id * geodes
    return quality


EXPECTED_TEST_RESULT = 33
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
