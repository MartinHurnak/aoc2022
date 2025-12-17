from collections import deque
import os
import sys
import re

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

monkey_regex = re.compile(r"""Monkey (\d+):
  Starting items: ([\d\,\s]*)
  Operation: new = (old|\d+) ([\+\-\*\/]) (old|\d+)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)""")


class Operation:
    def __init__(self, operand1, operator, operand2):
        self.operand1 = (lambda old: old) if operand1 == "old" else (lambda op: int(operand1))
        self.operator = operator
        self.operand2 = (lambda old: old) if operand2 == "old" else (lambda op: int(operand2))
        
    def execute(self, old):
        if self.operator == "+":
            return self.operand1(old) + self.operand2(old)
        if self.operator == "-":
            return self.operand1(old) - self.operand2(old)
        if self.operator == "*":
            return self.operand1(old) * self.operand2(old)

class Monkey:
    def __init__(self, monkeystring):
        res = monkey_regex.match(monkeystring)
        self.id = int(res.group(1))
        self.items = deque([int(item) for item in res.group(2).split(", ")])
        self.operation = Operation(res.group(3), res.group(4), res.group(5))
        self.test_divisible_by = int(res.group(6))
        self.monkey_if_true = int(res.group(7))
        self.monkey_if_false = int(res.group(8))
        self.inspections = 0

    def catch(self, items):
        self.items.extend(items)

    def take_turn(self, common_divisor):
        throws = {self.monkey_if_false: [], self.monkey_if_true: []}
        while self.items:
            item = self.items.popleft()
            item = self.operation.execute(item) # inspect
            item %= common_divisor # Chinese remainder theorem
            self.inspections += 1
            if item % self.test_divisible_by == 0: # test
                throws[self.monkey_if_true].append(item) # throw
            else:
                throws[self.monkey_if_false].append(item) # throw
        return throws

    def __lt__(self, other):
        return self.inspections < other.inspections

def main(filename):
    with open(filename) as f:
        data = f.read()

    monkeys = {}
    common_divisor = 1
    for monkeystring in data.split("\n\n"):
        monkey = Monkey(monkeystring)
        monkeys[monkey.id] = monkey
        # https://en.wikipedia.org/wiki/Chinese_remainder_theorem
        common_divisor *= monkey.test_divisible_by


    for i in range(10000):
        for monkey in monkeys.values():
            throws = monkey.take_turn(common_divisor)
            for other_monkey, items in throws.items():
                monkeys[other_monkey].catch(items)

    most_active_monkeys = sorted(monkeys.values(), reverse=True)
    
    return most_active_monkeys[0].inspections * most_active_monkeys[1].inspections


EXPECTED_TEST_RESULT = 2713310158
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
