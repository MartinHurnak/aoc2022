from collections import deque
import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

def in_map(map, x, y):
    return 0 <= x < len(map[0]) and 0 <= y < len(map)

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    map = []
    for row, line in enumerate(lines):
        map.append([])
        for col, c in enumerate(line.strip()):
            if c == "S":
                map[row].append(0)
                start = (col, row)
            elif c == "E":
                map[row].append(ord("z")-ord("a"))
                end = (col, row)
            else:
                map[row].append(ord(c) - ord("a"))
    
    # BFS from S to E
    queue = deque()
    queue.append((start, 0))
    visited = {start}
    while queue:
        current_pos, steps = queue.popleft()
        current_elev = map[current_pos[1]][current_pos[0]]
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if in_map(map, *new_pos) and new_pos not in visited:
                elev = map[new_pos[1]][new_pos[0]]
                if elev <= current_elev + 1:
                    if new_pos == end:
                        return steps + 1
                    queue.append((new_pos, steps+1))
                    visited.add(new_pos)

    return None


EXPECTED_TEST_RESULT = 31
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
