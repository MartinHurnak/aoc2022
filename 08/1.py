import os
import sys
import numpy as np

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    trees = [[int(c) for c in line.strip()] for line in lines]
    visible = np.zeros_like(trees)

    for i, row in enumerate(trees):
        left_max = -1
        right_max = -1
        for j in range(len(row)):
            if row[j] > left_max:
                visible[i][j] = 1
                left_max = row[j]
        
            if row[-j-1] > right_max:
                visible[i][-j-1] = 1
                right_max = row[-j-1]
        
    for j in range(len(trees[0])):
        top_max = -1
        bot_max = -1
        for i in range(len(trees)):
            if trees[i][j] > top_max:
                visible[i][j] = 1
                top_max = trees[i][j]
            
            if trees[-i-1][j] > bot_max:
                visible[-i-1][j] = 1
                bot_max = trees[-i-1][j]
                
    return np.sum(visible)


EXPECTED_TEST_RESULT = 21
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
