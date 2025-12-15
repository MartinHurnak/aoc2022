import os
import sys
import re

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

COL_WIDTH = 4

def main(filename):
    with open(filename) as f:
        data = f.read()

    stack_lines, moves = data.split("\n\n")
    stack_lines = stack_lines.split("\n")
    columns = (len(stack_lines[-1]) + 1) // COL_WIDTH
    stacks = [list() for _ in range(columns)]

    for col in range(columns):
        for line in reversed(stack_lines[:-1]):
            crate = line[col * COL_WIDTH + 1]
            if crate != ' ':
                stacks[col].append(crate)
    p = re.compile(r'move ([0-9]+) from ([0-9]+) to ([0-9]+)')
    for move in moves.split("\n"):
        crates, src, dst = (int(g) for g in p.match(move).groups())
        for _ in range(crates):
            stacks[dst-1].append(stacks[src-1].pop())    

    return "".join([stack[-1] if stack else " " for stack in stacks])


EXPECTED_TEST_RESULT = "CMZ"
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
