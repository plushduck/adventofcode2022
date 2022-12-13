DIR_OFFSETS = {
    'U': [0,1],
    'D': [0,-1],
    'L': [-1,0],
    'R': [1,0]
}

def update_tail_pos(tpos, hpos):
    offset = [hpos[0]-tpos[0],hpos[1]-tpos[1]]
    dist_sqr = offset[0]*offset[0] + offset[1]*offset[1]
    if dist_sqr > 2:
        offset[0] = max(min(offset[0],1),-1)
        offset[1] = max(min(offset[1],1),-1)
        tpos[0] += offset[0]
        tpos[1] += offset[1]


def part_1():
    visited = set()
    hpos = [0,0]
    tpos = [0,0]
    with open('./input.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            offset = DIR_OFFSETS[line[0]]
            count = int(line[2:])
            for i in range(0,count):
                hpos[0] += offset[0]
                hpos[1] += offset[1]
                update_tail_pos(tpos, hpos)
                visited.add(tuple(tpos))
    print(len(visited))

def part_2():
    visited = set()
    knots = []
    for i in range(10):
        knots.append([0,0])
    with open('./input.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            offset = DIR_OFFSETS[line[0]]
            count = int(line[2:])
            for i in range(0,count):
                knots[0][0] += offset[0]
                knots[0][1] += offset[1]
                for i in range(9):
                    update_tail_pos(knots[i+1], knots[i])
                visited.add(tuple(knots[9]))
    print(len(visited))


if __name__ == "__main__":
    part_2()