from enum import Enum
from functools import reduce
from typing import List,Tuple

# The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors.
# The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors.


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

DECODER = {
    "A": Shape.ROCK,
    "X": Shape.ROCK,
    "B": Shape.PAPER,
    "Y": Shape.PAPER,
    "C": Shape.SCISSORS,
    "Z": Shape.SCISSORS,
}

BEATEN_BY = {
    Shape.ROCK: Shape.PAPER,
    Shape.PAPER: Shape.SCISSORS,
    Shape.SCISSORS: Shape.ROCK,
}

BEATS = {key:val for val,key in BEATEN_BY.items()}

def parse_strategy_guide_1() -> List[Tuple[Shape, Shape]]:
    with open("./input.txt") as f:
        lines = f.read().splitlines()
    return [(DECODER[line[0]], DECODER[line[2]]) for line in lines]

# The winner of the whole tournament is the player with the highest score. 
# Your total score is the sum of your scores for each round. 
# The score for a single round is the score for the shape you selected 
# (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round
#  (0 if you lost, 3 if the round was a draw, and 6 if you won)
def score_round(round: Tuple[Shape, Shape]) -> int:
    their_shape = round[0]
    my_shape = round[1]
    if my_shape == their_shape:
        return 3 + my_shape.value
    if BEATEN_BY[their_shape] == my_shape:
        return 6 + my_shape.value
    return my_shape.value

def part_1():
    rounds = parse_strategy_guide_1()
    print(reduce(lambda score, round: score + score_round(round), rounds, 0))

# "Anyway, the second column says how the round needs to end: 
# X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

def parse_strategy_guide_2() -> List[Tuple[Shape, Shape]]:
    with open("./input.txt") as f:
        lines = f.read().splitlines()
        parsed_rounds = []
        for line in lines:
            their_shape = DECODER[line[0]]
            if line[2] == "X":
                # Lose
                parsed_rounds.append((their_shape,BEATS[their_shape]))
            elif line[2] == "Y":
                parsed_rounds.append((their_shape, their_shape))
            else:
                parsed_rounds.append((their_shape, BEATEN_BY[their_shape]))
    return parsed_rounds

def part_2():
    rounds = parse_strategy_guide_2()
    print(reduce(lambda score, round: score + score_round(round), rounds, 0))

if __name__ == "__main__":
    part_1()
    part_2()