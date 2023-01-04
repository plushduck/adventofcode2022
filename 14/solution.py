from functools import reduce

# 498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9
def parse_input(filename):
    max_y = -1
    with open(filename) as f:
        lines = f.read().splitlines()
        paths = []
        for l in lines:
            path = [c.split(',') for c in l.split(' -> ')]
            path = [(int(c[0]),int(c[1])) for c in path]
            max_y = max(max_y, max([c[1] for c in path]))
            paths.append(path)
        return paths, max_y

def paths_to_points(paths):

    points = set()

    def add_path_segment(c1, c2):
        if c1[0] > c2[0]:
            for i in range(c2[0],c1[0]+1):
                points.add((i,c1[1]))
        elif c2[0] > c1[0]:
            for i in range(c1[0],c2[0]+1):
                points.add((i,c1[1]))
        elif c1[1] > c2[1]:
            for i in range(c2[1],c1[1]+1):
                points.add((c1[0],i))
        elif c2[1] > c1[1]:
            for i in range(c1[1],c2[1]+1):
                points.add((c1[0],i))

    for path in paths:
        for i in range(len(path)-1):
            add_path_segment(path[i],path[i+1])

    return points

def next_resting_point(points, max_y):
    pos = [500,0]
    while True:
        if tuple([pos[0],pos[1]+1]) not in points:
            pos[1] += 1
        elif tuple([pos[0]-1,pos[1]+1]) not in points:
            pos[0] -= 1
            pos[1] += 1
        elif tuple([pos[0]+1,pos[1]+1]) not in points:
            pos[0] += 1
            pos[1] += 1
        else:
            return tuple(pos)
        if pos[1] == max_y:
            return tuple(pos)

def part_1(filename):
    print(f"Part 1: {filename}")
    paths, max_y = parse_input(filename)
    points = paths_to_points(paths)
    sand_dropped = 0
    while(True):
        sand_pos = next_resting_point(points, max_y)
        if sand_pos[1] == max_y:
            print(f"{sand_dropped}, FINAL ANSWER")
            return
        sand_dropped += 1
        # print(sand_pos)
        points.add(sand_pos)

def part_2(filename):
    print(f"Part 2: {filename}")
    paths, max_y = parse_input(filename)
    points = paths_to_points(paths)
    sand_dropped = 0
    while(True):
        sand_pos = next_resting_point(points, 1+max_y)
        sand_dropped += 1
        if sand_pos == (500,0):
            print(f"{sand_dropped}, FINAL ANSWER")
            return
        points.add(sand_pos)

# 774
part_1('./input.txt')
# 22499
part_2('./input.txt')
