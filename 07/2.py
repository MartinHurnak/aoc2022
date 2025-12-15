from collections import defaultdict
import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")



FS_SIZE = 70000000
SPACE_NEEDED = 30000000

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    # Gather directory sizes (count only non-dir files)
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

    # Accumulate dir sizes recursively (including nested dirs)
    total_sizes = {}
    for dir in dirs.keys():
        total_size = 0
        for other_dir in dirs.keys():
            if other_dir[:len(dir)] == dir:
                total_size += dirs[other_dir]
        total_sizes[dir] = total_size

    # Search for smallest dir to delete
    free_space = FS_SIZE - total_sizes[("/", )]

    dir_to_delete = ("/", )
    for dir, size in total_sizes.items():
        if size < SPACE_NEEDED - free_space:
            continue
        if size < total_sizes[dir_to_delete]:
            dir_to_delete = dir

    return total_sizes[dir_to_delete]

EXPECTED_TEST_RESULT = 24933642
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
