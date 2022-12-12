class tree():
    def __init__(self, height):
        self.height = height
        self.blocked_left = False
        self.blocked_right = False
        self.blocked_up = False
        self.blocked_down = False

    def blocked(self):
        return self.blocked_left and self.blocked_right and self.blocked_up and self.blocked_down


FOREST = []

def parse_forest():
    forest = []
    with open('./input.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            FOREST.append([tree(int(c)) for c in line])

parse_forest()

def part_1():
    tallest = -1
    for row in FOREST:
        tallest = -1
        for tree in row:
            if tree.height <= tallest:
                tree.blocked_left = True
            tallest = max(tallest,tree.height)
        tallest = -1
        for tree in row[::-1]:
            if tree.height <= tallest:
                tree.blocked_right = True
            tallest = max(tallest,tree.height)
    ncols = len(FOREST[0])
    for i in range(0,ncols):
        tallest = -1
        for row in FOREST:
            tree = row[i]
            if tree.height <= tallest:
                tree.blocked_up = True
            tallest = max(tallest,tree.height)
    for i in range (0,ncols):
        tallest = -1
        for row in FOREST[::-1]:
            tree = row[i]
            if tree.height <= tallest:
                tree.blocked_down = True
            tallest = max(tallest,tree.height)

    nvisible = 0
    for row in FOREST:
        for tree in row:
            if not (tree.blocked()):
                nvisible += 1
    print(nvisible)


if __name__ == "__main__":
    part_1()

