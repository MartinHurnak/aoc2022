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

    input1, operator, input2 = results["root"]

    input1_G = G.subgraph(nx.ancestors(G, input1) | {input1})
    input2_G = G.subgraph(nx.ancestors(G, input2) | {input2})

    if "humn" in input1_G:
        humn_G = input1_G
        solvable_input = input2
    else:
        humn_G = input2_G
        solvable_input = input1

    humn_descendants = nx.descendants(G, "humn")

    # solve everything except humn descendants
    for node in nx.topological_sort(G):
        result = results[node]
        if isinstance(result, int):
            continue
        if node in humn_descendants:
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


    result = results[solvable_input]

    # now solve humn subgraph in reverse order to figure out how to get matching inputs
    for node in reversed(list(nx.topological_sort(humn_G))): 
        if isinstance(results[node], int):
            continue
        input1, operator, input2 = results[node]
        if isinstance(results[input1], int) and input1 != "humn":
            if operator == "+":
                result = result - results[input1]
            elif operator == "-":
                result = results[input1] - result
            elif operator == "*":
                result = result // results[input1]
            elif operator == "/":
                result = results[input1] // result
        else:
            if operator == "+":
                result = result - results[input2]
            elif operator == "-":
                result = results[input2] + result
            elif operator == "*":
                result = result // results[input2]
            elif operator == "/":
                result = results[input2] * result


        if input1 == "humn" or input2 == "humn":
            return result


EXPECTED_TEST_RESULT = 301
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
