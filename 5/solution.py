from functools import reduce
import re

def parse_input():
    with open('./input.txt') as f:
        lines = f.read().splitlines()

        # Determine number of stacks
        no_stacks = int((len(lines[0])+1)/4)
        stacks = []
        for i in range(no_stacks):
            stacks.append([])

        # Parse the stacks
        # Example: "        [Q] [M]     [J] [R] [W] [H]"
        i = 0
        while lines[i].find('[') != -1:
            crates = lines[i]
            for j in range(0,no_stacks):
                if crates[j*4] == '[':
                    contents = crates[j*4+1]
                    stacks[j].append(crates[j*4+1])
            i += 1

        # Skip line of crate numbers and empty line
        i += 2

        # Parse the moves list
        # Example: "move 1 from 2 to 1"
        moves = []
        move_regex = re.compile(r'move (?P<count>\d+) from (?P<src>\d+) to (?P<dst>\d+)')
        for line in lines[i:]:
            m = move_regex.match(line)
            count = int(m.group('count'))
            src = int(m.group('src'))
            dst = int(m.group('dst'))
            moves.append((count, src, dst))

        # Reverse stacks so "bottom" item is first
        for stack in stacks:
            stack.reverse()

        return stacks, moves

def apply_moves(stacks, moves, single_crate = True):
    for move in moves:
        count, src, dst = move
        if single_crate:
            for i in range(0,count):
                stacks[dst-1].append(stacks[src-1].pop())
        else:
            stacks[dst-1] += stacks[src-1][-1*count:]
            stacks[src-1] = stacks[src-1][:-1*count]


def part_1():
    print("PART 1")
    stacks, moves = parse_input()
    apply_moves(stacks, moves)
    stack_tops = reduce(lambda accum, stack: accum + stack[-1], stacks, "")
    print(stack_tops)

def part_2():
    print("PART 2")
    stacks, moves = parse_input()
    apply_moves(stacks, moves, single_crate=False)
    stack_tops = reduce(lambda accum, stack: accum + stack[-1], stacks, "")
    print(stack_tops)

if __name__ == "__main__":
    part_1()
    part_2()
