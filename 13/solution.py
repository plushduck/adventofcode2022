from enum import Enum, auto
from pprint import PrettyPrinter

pprint = PrettyPrinter(indent=2).pprint


class Result(Enum):
    IN_ORDER = auto()
    OUT_OF_ORDER = auto()
    UNDETERMINED = auto()

def parse_line(line):
    parse_stack = [[]]
    number = ''
    for char in line[1:]:
        if char == '[':
            parse_stack.append([])
        elif char == ']':
            if number != '':
                parse_stack[-1].append(int(number))
                number = ''
            e = parse_stack.pop()
            if not parse_stack:
                return e
            parse_stack[-1].append(e)
        elif char != ',':
            number += char
        elif char == ',':
            if number != '':
                parse_stack[-1].append(int(number))
                number = ''

def in_order(item1, item2, indent = 0):

    prefix = "" + "  " * indent
    # print(prefix + f"Compare {item1} vs {item2}")

    if isinstance(item1, int) and isinstance(item2, int):
        if item1 < item2:
            return Result.IN_ORDER
        if item1 > item2:
            return Result.OUT_OF_ORDER
        return Result.UNDETERMINED

    if isinstance(item1, list) and isinstance(item2, list):
        to_compare = min(len(item1), len(item2))
        for i in range(0,to_compare):
            i_result = in_order(item1[i], item2[i], indent + 1)
            if i_result != Result.UNDETERMINED:
                return i_result
        if len(item1) == len(item2):
            return Result.UNDETERMINED
        if len(item1) < len(item2):
            return Result.IN_ORDER
        return Result.OUT_OF_ORDER
    if isinstance(item1, list) and isinstance(item2, int):
        return in_order(item1, [item2], indent + 1)
    if isinstance(item1, int) and isinstance(item2, list):
        return in_order([item1], item2, indent + 1)

    assert False


TEST_CASES = [
    ['[1,1,3,1,1]', '[1,1,5,1,1]', Result.IN_ORDER],
    ['[[1],[2,3,4]]', '[[1],4]', Result.IN_ORDER],
    ['[[1],4]', '[[1],[2,3,4]]', Result.OUT_OF_ORDER],
    ['[9]','[[8,7,6]]', Result.OUT_OF_ORDER],
    ['[[4,4],4,4]','[[4,4],4,4,4]', Result.IN_ORDER],
    ['[7,7,7,7]','[7,7,7]', Result.OUT_OF_ORDER],
    ['[]','[3]', Result.IN_ORDER],
    ['[[[]]]', '[[]]', Result.OUT_OF_ORDER]
]

'[[[10,[],5,[5,10,2,10,5]]],[[[4,1,2,5],1,2,9],[4,10],[],[]],[[],8,[[7],7]],[[[8],7,8,3]],[7,5]]'
'[[5,[[9,4],9],[7,[6,4],[1,9,9,3,10]],2,2],[[3,[],1,9]],[[8,[5],2,[10,3,8,8]],4,[],10,[5,9]],[[[],4,[7,8,6]],[[2,2,1,8,5],[0,10,6,6]],[7,[7,9,9,7],8,6]]]'


def run_tests():
    for test_case in TEST_CASES:
        input1 = parse_line(test_case[0])
        input2 = parse_line(test_case[1])
        result = in_order(input1, input2)
        # print(result)
        assert result == test_case[2]

run_tests()

# 3794 TOO Low
# 5777 TOO HIGH
# 5988 TOO HIGH
def part_1():
    with open('./input.txt') as f:
        lines = f.read().splitlines()
        output = 0
        for i in range(0,int(len(lines)/3)+1):
            input1 = parse_line(lines[3*i])
            input2 = parse_line(lines[3*i+1])
            result = in_order(input1, input2)
            assert result != Result.UNDETERMINED
            if result == Result.IN_ORDER:
                output += (i+1)
        assert output == 5684
        print(output)

part_1()

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def packets_cmp(p1,p2):
    result = in_order(p1,p2)
    if result == Result.IN_ORDER:
        return -1
    if result == Result.OUT_OF_ORDER:
        return 1
    return 0

def part_2():
    with open('./input.txt') as f:
        lines = f.read().splitlines()
        packets = []
        for l in lines:
            if l != "":
                packets.append(parse_line(l))
        packets.extend([[[2]],[[6]]])
        packets = sorted(packets, key=cmp_to_key(packets_cmp))
        i1 = packets.index([[2]])+1
        i2 = packets.index([[6]])+1
        print(i1*i2)

part_2()
