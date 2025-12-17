import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

class Packet:
    def __init__(self, data):
        self.data = data
    
    def __eq__(self, other):
        return self.data == other.data
    
    def __lt__(self, other):
        for l, r in zip(self.data, other.data):
            if not (isinstance(l, int) and isinstance(r, int)):
                l = Packet([l]) if not isinstance(l, list) else Packet(l)
                r = Packet([r]) if not isinstance(r, list) else Packet(r)
            if l == r:
                continue
            return l < r
        if len(self.data) != len(other.data):
            return len(self.data) < len(other.data)

def main(filename):
    with open(filename) as f:
        data = f.read()

    pairs = data.split("\n\n")

    packets = [Packet([[2]]), Packet([[6]])] # divider packets
    for pair in pairs:
        for data in pair.split("\n"):
            packets.append(Packet(eval(data)))
    
    packets.sort()

    # +1 since index in assignment starts at 1
    return (packets.index(Packet([[2]])) + 1) * (packets.index(Packet([[6]])) + 1)



EXPECTED_TEST_RESULT = 140
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
