from functools import reduce
from typing import Set

def get_priority(s):
    ascii_value = ord(s)
    # Lowercase item types a through z have priorities 1 through 26.
    # Uppercase item types A through Z have priorities 27 through 52.
    if ascii_value < 91:
        # Upper Case, 'A' == 65
        return ascii_value - 38
    else:
        # Lower Case, 'a' == 97
        return ascii_value - 96

def part_1():
    print("PART 1:")
    with open("./input.txt") as f:
        lines = f.read().splitlines()
        total = 0
        for line in lines:
            index = int(len(line)/2)
            contents_1 = set(line[:index])
            contents_2 = set(line[index:])
            common_item= (contents_1 & contents_2).pop()
            total += get_priority(common_item)
        print(total)

def part_2():
    print("PART 2:")

    with open("./input.txt") as f:
        lines = f.read().splitlines()
        total = 0

        for i in range(0, len(lines), 3):
            badge_item = set(lines[i]) & set(lines[i+1]) & set(lines[i+2])
            total += get_priority(badge_item.pop())
        print(total)

if __name__ == "__main__":
    part_1()
    part_2()
