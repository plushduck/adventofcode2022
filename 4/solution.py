import re


def parse_input():
    regex = re.compile(r'(?P<s1>\d+)-(?P<e1>\d+),(?P<s2>\d+)-(?P<e2>\d+)')
    with open('./input.txt') as f:
        parsed = []
        lines = f.read().splitlines()
        for l in lines:
            m = regex.match(l)
            s1_start = int(m.group('s1'))
            s1_end = int(m.group('e1'))
            s2_start = int(m.group('s2'))
            s2_end = int(m.group('e2'))
            parsed.append([(s1_start,s1_end),(s2_start,s2_end)])
        return parsed
ASSIGNMENT_PAIRS = parse_input()

def fully_overlap(ap):
        if ap[0][0] <= ap[1][0] and ap[0][1] >= ap[1][1]:
            return True
        if ap[1][0] <= ap[0][0] and ap[1][1] >= ap[0][1]:
            return True
        return False

def part_1():
    print("PART 1:")
    print(sum(map(fully_overlap, ASSIGNMENT_PAIRS)))

def overlap(ap):
    if ap[0][0] <= ap[1][0] and ap[0][1] >= ap[1][0]:
        return True
    if ap[1][0] <= ap[0][0] and ap[1][1] >= ap[0][0]:
        return True
    return False

def part_2():
    print("PART 2:")
    print(sum(map(overlap, ASSIGNMENT_PAIRS)))

if __name__ == "__main__":
    part_1()
    part_2()
