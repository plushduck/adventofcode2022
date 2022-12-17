from abc import ABC, abstractmethod
from collections import deque
from functools import reduce
import operator as op
import re


class Monkey:

    def __init__(self, start_items, operation, divisor, divisible_target, indivisible_target):

        self.item_queue = deque(reversed(start_items))
        self.inspections = 0
        self.operation = operation
        self.divisor = divisor
        self.divisible_target = divisible_target
        self.indivisible_target = indivisible_target
        self.worry_modulo = None

    def inspect(self):
        self.inspections += 1
        worry = self.item_queue.pop()
        # print(f"  Monkey inspects an item with worry level of {worry}")
        worry = self.operation(worry)
        # worry = worry // 3
        if self.worry_modulo is not None:
            worry = worry % self.worry_modulo
##        print(f"    Monkey gest bored with item. Worry level is divided by 3 to {worry}")
        if worry % self.divisor == 0:
            # print(f"    Current worry level is divisible by {self.divisor}")
            # print(f"    Item with worry level {worry} is thrown to monkey {self.divisible_target}")
            return worry, self.divisible_target
        else:
            # print(f"    Current worry level is not divisible by {self.divisor}")
            # print(f"    Item with worry level {worry} is thrown to monkey {self.indivisible_target}")
            return worry, self.indivisible_target

class MonkeyTroop:

    def __init__(self, monkey_list):
        self.monkey_list = monkey_list

    def monkey_turn(self, monkey):
        while monkey.item_queue:
            worry, target = monkey.inspect()
            self.monkey_list[target].item_queue.appendleft(worry)

    def monkey_round(self):
        for monkey in self.monkey_list:
            self.monkey_turn(monkey)

    def print(self):
        for i, monkey in enumerate(self.monkey_list):
            item_str = ' '.join([str(item) for item in monkey.item_queue])
            print(f"Monkey {i}: {monkey.item_queue}")

operation_regex = re.compile(r'(?P<operand1>.+)(?P<operator>[*+])(?P<operand2>.+)')

def parse_operation(operation_str):
    operation_str = operation_str.replace(" ","")
    m = operation_regex.match(operation_str)
    operand1_str = m.group('operand1')
    operator_str = m.group('operator')
    operand2_str = m.group('operand2')

    def f(worry):
        operand1 = worry if operand1_str == "old" else int(operand1_str)
        operator = op.add if operator_str == "+" else op.mul
        operand2 = worry if operand2_str == "old" else int(operand2_str)
        return operator(operand1,operand2)

    return f

def parse_monkey(lines):
    items_str = lines[1][len("  Starting items: "):]
    items_str = items_str.replace(" ", "")
    items = [int(item_str) for item_str in items_str.split(",")]

    operation_str = lines[2][len("  Operation: new = "):]
    operation = parse_operation(operation_str)

    divisor = int(lines[3][len("  Test: divisible by "):])
    divisible_target = int(lines[4][len("    If true: throw to monkey "):])
    indivisible_target = int(lines[5][len("    If false: throw to monkey "):])
    return Monkey(items, operation, divisor, divisible_target, indivisible_target)

def parse_troop():
    monkeys = []
    with open('./input.txt') as f:
        lines = f.read().splitlines()
        for i in range(0, len(lines)//7 + 1):
            monkeys.append(parse_monkey(lines[7*i: 7*(i+1)]))

    return MonkeyTroop(monkey_list = monkeys)

def part_1():
    # Problem Answer = 55944
    # Test Answer = 10605

    troop = parse_troop()

    for i in range(0,20):
        troop.monkey_round()
        print(f"After round {i+1}, the monkeys are holding items ith these worry levels:")
        #troop.print()

    for i in range(0,4):
        print(f"Monkey {i} inspected items {troop.monkey_list[i].inspections}")

    inspections = sorted([monkey.inspections for monkey in troop.monkey_list])
    monkey_business = inspections[-1]*inspections[-2]
    print (f"monkey_business = {monkey_business}")

def part_2():
    # Problem Answer = 15117269860
    # Test Answer = 2713310158

    troop = parse_troop()

    monkey_divisors = [monkey.divisor for monkey in troop.monkey_list]
    monkey_gcf = reduce(lambda x,y: x*y, monkey_divisors)
    print(f"monkey_gcf = {monkey_gcf}")

    for monkey in troop.monkey_list:
        monkey.worry_divisor = 1
        monkey.worry_modulo = monkey_gcf

    for i in range(0,10000):
        troop.monkey_round()
        if i == 0 or i == 19 or (i+1)%1000 == 0:
            print(f"After round {i+1}:")
            for i in range(0,4):
                print(f"Monkey {i} inspected items {troop.monkey_list[i].inspections}")


    inspections = sorted([monkey.inspections for monkey in troop.monkey_list])
    monkey_business = inspections[-1]*inspections[-2]
    print (f"monkey_business = {monkey_business}")

part_2()
