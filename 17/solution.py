from copy import deepcopy
import operator as op

# The Rocks:

# ####

# .#.
# ###
# .#.

# ..#
# ..#
# ###

# #
# #
# #
# #

# ##
# ##

class Rock:
    def __init__(self, shape):
        self.shape = shape

rock_types = [
    [0b000111100
    ],
    [0b000010000,
     0b000111000,
     0b000010000
    ],
    [0b000001000,
     0b000001000,
     0b000111000
    ],
    [0b000100000,
     0b000100000,
     0b000100000,
     0b000100000,
    ],
    [0b000110000,
     0b000110000,
    ],
]

with open('./test.txt') as f:
    moves = f.read().splitlines()[0]

move_ops = {
    '>': op.irshift,
    '<': op.ilshift,
}

MAP = [0b111111111]
def print_map(rock=None, rock_index=None, really = False):
    if not really:
        return
    for i in range(len(MAP[:-8])):
        mstr = f'{MAP[-1*i-1]:09b}'
        # print(f"MSTR = {mstr}")
        ri = len(MAP) - i -1
        # print(f"i = {i}")
        # print(f"ri = {ri}")
        # print(f"rock_index = {rock_index}")
        if rock:
            if ri >= rock_index and ri < rock_index + len(rock):
                rstr = f'{rock[-1*(ri-rock_index)-1]:09b}'
                # print(f"RSTR = {rstr}")
                cstr = ""
                for j in range(0,9):
                    if rstr[j] == '1':
                        assert mstr[j] == '0'
                        cstr += '@'
                    else:
                        cstr += mstr[j]
                mstr = cstr
        print('|' + mstr[1:8] + '|')


def print_rock(rock):
    for r in rock:
        print(f'{r:09b}')


def part_1():

    move_index = 0
    global MAP

    for round in range(0,2022):

        # Ye Olde Rock
        rock_type = rock_types[round%len(rock_types)]
        rock = deepcopy(rock_type)

        # Add 3 empty line + lines the rock occupies
        MAP.extend([0b100000001]*(3+len(rock)))
        rock_level = len(MAP) - len(rock)
        # print(f"ROCK LEVEL = {rock_level}")

        print("")
        print(f"ROCK {round + 1} ADDED")
        print("")

        rock_stopped = False
        while not rock_stopped:

            print_map(rock, rock_level)

            # Attempt to move the rock
            move = moves[move_index%len(moves)]
            print("move = " + move)
            move_index += 1
            new_rock = [move_ops[move](r,1) for r in rock]

            # print("")
            # print("NEW ROCK:")
            # print_rock(new_rock)
            # print("")

            collision = False
            for i,r in enumerate(new_rock):
                print(f'{new_rock[i]:09b} vs {MAP[rock_level+len(new_rock)-i-1]:09b}')
                if new_rock[i] & MAP[rock_level+len(new_rock)-i-1]:
                    collision = True
                    break
            if not collision:
                rock = deepcopy(new_rock)

            print_map(rock, rock_level)

            # Attempt to drop:
            for j in range(0,len(rock)):
                if rock[(j+1)*-1] & MAP[rock_level-1+j]:
                    if not rock_stopped:
                        print("ROCK STOPPED")
                    rock_stopped = True
                    # print(f"ROCK LEVEL = {rock_level}")

                    # Add the rock to the map
                    for i in range(0, len(rock)):
                        # print(len(rock))
                        # print(i)
                        # print(f'{MAP[rock_level + i]:09b}')
                        # print(f'{rock[i*-1]:09b}')
                        MAP[rock_level + i] |= rock[(i+1)*-1]
                        # print(f'{MAP[rock_level + i]:09b}')
                        # print(i)
            if not rock_stopped:
                rock_level -= 1
                if not MAP[-1] & 0b011111110:
                    MAP.pop()
            # print_map()
            # input()
        # print_map()
        # print(f"Round {round}, {len(MAP)}")

part_1()
print_map(really=True)
print(len(MAP)-1)

# 3176 is too low