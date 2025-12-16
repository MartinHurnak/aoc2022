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

    best_scenic_score = 0
    for i, row in enumerate(trees):
        for j, tree in enumerate(row):
            left_score, right_score, up_score, down_score = 0, 0, 0, 0
            
            for x in range(j-1, -1, -1):
                left_score += 1
                if row[x] >= tree:
                    break

            for x in range(j+1, len(row)):
                right_score += 1
                if row[x] >= tree:
                    break
            
            for y in range(i-1, -1, -1):
                up_score += 1
                if trees[y][j] >= tree:
                    break
            
            for y in range(i+1, len(trees)):
                down_score += 1
                if trees[y][j] >= tree:
                    break
            
            best_scenic_score = max(best_scenic_score,  left_score * right_score * up_score * down_score )
                
    return best_scenic_score


EXPECTED_TEST_RESULT = 8
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
