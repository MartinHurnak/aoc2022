import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    # reverse, so we can pop them in correct order
    lines = list(reversed([line.strip() for line in lines]))

    X = 1
    cycle = 0
    cycles_to_finish = 0
    instruction = None
    result = ""
    while lines:
        if cycles_to_finish == 0:
            if instruction and instruction.startswith("addx"):
                X += int(instruction[5:])
            instruction = lines.pop()
            if instruction.startswith("addx"):
                cycles_to_finish = 2
            else:
                cycles_to_finish = 1
        
        if cycle % 40 == 0:
            result += "\n"

        if X - 1 <= cycle % 40 <= X + 1:
            result += "#"
        else:
            result += "."

        cycle += 1
        cycles_to_finish -= 1

    return result + "\n"


EXPECTED_TEST_RESULT = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
