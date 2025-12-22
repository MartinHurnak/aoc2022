import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

DECRYPTION_KEY = 811589153

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    code = [int(l.strip()) * DECRYPTION_KEY for l in lines]
    orig_index_0 = code.index(0)
    index = list(range(len(code)))

    # the idea here is to create two arrays one will contain original elements and one will contain index of each element
    # instead of shuffling actual values, we just iterate over them and modify indexes using simple increment/decrement

    for _ in range(10):
        for i in range(len(code)):
            original_index = index[i]
            index[i] = (original_index + code[i])
            # based on examples, numbers don't end up on the start of the list, but are wrapped to the end instead 
            if index[i] == 0:
                index[i] -= 1
                index[i] %= len(code)
            else:
                index[i] %= len(code) - 1

            for j in range(len(index)):
                if original_index < index[i]:
                    if original_index < index[j] <= index[i] and i != j:
                        index[j] -=1
                else:
                    if index[i] <= index[j] < original_index and i != j:
                        index[j] += 1

    result = 0
    index_0 = index[orig_index_0]
    for nth in [1000, 2000, 3000]:
        result += code[index.index((index_0 + nth) % len(index))]

    return result


EXPECTED_TEST_RESULT = 1623178306
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
