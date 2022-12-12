class tree():
    def __init__(self, height):
        self.height = height
        self.blocked_left = False
        self.blocked_right = False
        self.blocked_up = False
        self.blocked_down = False
        self.scenic_score = 1

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


def part_2():
    nrows = len(FOREST)
    ncols = len(FOREST[0])
    for r in range(0,nrows):
        # last blocker at a given height
        visibility = [1]*10
        FOREST[r][0].scenic_score = 0
        FOREST[r][ncols-1].scenic_score = 0
        for c in range(1,ncols):
            tree = FOREST[r][c]
            height = tree.height
            tree.scenic_score *= visibility[height]
            for i in range(0,height+1):
                visibility[i] = 1
            for i in range(height+1, 10):
                visibility[i] += 1
        visibility = [1]*10
        for c in range(ncols-2,-1,-1):
            tree = FOREST[r][c]
            height = tree.height
            tree.scenic_score *= visibility[height]
            for i in range(0,height+1):
                visibility[i] = 1
            for i in range(height+1, 10):
                visibility[i] += 1
    for c in range(0,ncols):
        visibility = [1]*10
        FOREST[0][c].scenic_score = 0
        FOREST[nrows-1][c].scenic_score = 0
        for r in range (1,nrows):
            tree = FOREST[r][c]
            height = tree.height
            tree.scenic_score *= visibility[height]
            for i in range(0,height+1):
                visibility[i] = 1
            for i in range(height+1, 10):
                visibility[i] += 1
        visibility = [1]*10
        for r in range(nrows-2,-1,-1):
            tree = FOREST[r][c]
            height = tree.height
            tree.scenic_score *= visibility[height]
            for i in range(0,height+1):
                visibility[i] = 1
            for i in range(height+1, 10):
                visibility[i] += 1

    max_score = max([max([t.scenic_score for t in row]) for row in FOREST])
    print(max_score)


if __name__ == "__main__":
    part_2()

