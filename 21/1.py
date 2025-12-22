import os
import sys
import re
import networkx as nx

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

pattern = re.compile(r"([a-z]{4}) ([\+\-\*\/]) ([a-z]{4})")

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    G = nx.DiGraph()

    results = {}
    for line in lines:
        node_id, value = line.strip().split(":")
        try:
            value = int(value)
            G.add_node(node_id)
            results[node_id] = value
        except ValueError:
            input1, operator, input2 = pattern.match(value.strip()).groups()
            results[node_id] = (input1, operator, input2)
            G.add_node(node_id)
            G.add_edge(input1, node_id)
            G.add_edge(input2, node_id)
    
    for node in nx.topological_sort(G):
        result = results[node]
        if isinstance(result, int):
            continue
        input1, operator, input2 = result
        if operator == "+":
            results[node] = results[input1] + results[input2]
        elif operator == "-":
            results[node] = results[input1] - results[input2]
        elif operator == "*":
            results[node] = results[input1] * results[input2]
        elif operator == "/":
            results[node] = results[input1] // results[input2]
        
    return results["root"]


EXPECTED_TEST_RESULT = 152
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
