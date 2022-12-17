from collections import deque

def parse_heightmap(filename):
    hm = []
    start = None
    dest = None
    a_set = set()
    with open(filename) as f:
        lines = f.read().splitlines()
        for y,l in enumerate(lines):
            row = []
            for x,c in enumerate(l):
                if c == 'S':
                    start = (x,y)
                    row.append(0)
                    continue
                elif c == 'E':
                    dest = (x,y)
                    row.append(26)
                    continue
                if c == 'a':
                    a_set.add((x,y))
                row.append(ord(c)-ord('a')+1)
            hm.append(row)
    # print(f"start = {start}")
    # print(f"dest = {dest}")
    # for row in hm:
    #     print(row)
    return hm, start, dest, a_set

def legal_moves(hm, cur):
    pos_to_consider = [(cur[0]-1,cur[1]),(cur[0]+1,cur[1]),(cur[0],cur[1]+1),(cur[0],cur[1]-1)]
    legal_pos = set()
    for pos in pos_to_consider:
        if pos[0] < 0 or pos[0] >= len(hm[0]):
            continue
        if pos[1] < 0 or pos[1] >= len(hm):
            continue
        v1 = hm[pos[1]][pos[0]]
        v2 = hm[cur[1]][cur[0]]
        if hm[pos[1]][pos[0]] <= hm[cur[1]][cur[0]]+1:
            legal_pos.add(pos)
    return legal_pos

def print_costs(pos_costs):
    for y in range(0,5):
        row = ""
        for x in range(0,8):
            if (x,y) in pos_costs:
                c = pos_costs[(x,y)]
                if c < 10:
                    row += " "
                row += str(c)
            else:
                row += 'x'
            row += " "
        print(row)

def part_1(filename):
    hm,start,dest,_ = parse_heightmap(filename)
    visited = set()
    next_visits = {start}
    steps = 0
    pos_costs = {}

    while (True):
        lm = set()
        for pos in next_visits:
            pos_costs[pos] = steps
            lm.update(legal_moves(hm,pos))
        lm -= visited
        if dest in lm:
            return steps+1
        visited |= next_visits
        next_visits.clear()
        next_visits.update(lm)
        steps += 1

assert part_1('./test.txt') == 31
assert part_1('./input.txt') == 490

def part_2(filename):
    hm,start,dest,next_visits = parse_heightmap(filename)
    visited = set()
    steps = 0
    pos_costs = {}

    while (True):
        lm = set()
        for pos in next_visits:
            pos_costs[pos] = steps
            lm.update(legal_moves(hm,pos))
        lm -= visited
        if dest in lm:
            return steps+1
        visited |= next_visits
        next_visits.clear()
        next_visits.update(lm)
        steps += 1

assert part_2('./test.txt') == 29
print(part_2('./input.txt'))
