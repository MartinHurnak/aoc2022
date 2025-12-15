from collections import defaultdict
import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")



SIZE_LIMIT = 100000

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    path = []
    dirs = defaultdict(int)
    for line in lines:
        line = line.strip()
        if line.startswith("$ cd"):
            dir = line.split(" ")[2]
            if dir == "..":
                path.pop()
            elif dir == "/":
                path = ["/"]
            else:
                path.append(dir)
        elif line.startswith("$ ls"):
            continue
        else:
            size, name = line.split(" ")
            if size == "dir":
                dirs[tuple(path + [name])] = 0
            else:
                dirs[tuple(path)] += int(size)

    total_sizes_below_limit = 0
    for dir in dirs.keys():
        total_size = 0
        for other_dir in dirs.keys():
            if other_dir[:len(dir)] == dir:
                total_size += dirs[other_dir]
        if total_size <= SIZE_LIMIT:
            total_sizes_below_limit += total_size


    return total_sizes_below_limit


EXPECTED_TEST_RESULT = 95437
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
