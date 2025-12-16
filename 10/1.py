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

    X = 1
    cycle = 0
    signal_stregth = 0
    for line in lines:
        line = line.strip()
        if line == "noop":
            cycle += 1
        elif line.startswith("addx"):
            if (cycle - 20) % 40 == 39:
                signal_stregth += X * (cycle + 1)
            addx = int(line[5:])
            cycle += 2
         
        if (cycle - 20) % 40 == 0:
            signal_stregth += X * cycle

        X += addx
        addx = 0


    return signal_stregth


EXPECTED_TEST_RESULT = 13140
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
