from typing import NamedTuple
from dataclasses import dataclass
import re

BEACONS = []
SENSORS = []

@dataclass
class Sensor:
    x: int
    y: int
    m: int

    def no_beacon_segment(self, y:int):
        dist_to_y = abs(self.y-y)
        if dist_to_y > self.m:
            return None
        offset = self.m-dist_to_y
        return (self.x-offset,self.x+offset)

def manhattan(t1,t2):
    return(abs(t1[0]-t2[0]) + abs(t1[1]-t2[1]))

def parse_input(filename):
    global BEACONS
    global SENSORS
    BEACONS = []
    SENSORS = []
    sensor_x_re = r'Sensor at x=(?P<sx>-?\d+)'
    sensor_y_re = r', y=(?P<sy>-?\d+)'
    beacon_x_re = r': closest beacon is at x=(?P<bx>-?\d+)'
    beacon_y_re = r', y=(?P<by>-?\d+)'
    regex = sensor_x_re+sensor_y_re+beacon_x_re+beacon_y_re
    parse_regex = re.compile(regex)
    with open(filename) as f:
        lines = f.read().splitlines()
        xmin = None
        xmax = None
        for line in lines:
            m = parse_regex.match(line)
            sx = int(m.group('sx'))
            sy = int(m.group('sy'))
            bx = int(m.group('bx'))
            by = int(m.group('by'))
            if xmin is None:
                xmin = min(sx,bx)
            else:
                xmin = min(xmin,sx,bx)
            if xmax is None:
                xmax = max(sx,bx)
            else:
                xmax = max(sx,bx,xmax)
            BEACONS.append((bx,by))
            SENSORS.append(Sensor(x=sx,y=sy,m=manhattan((sx,sy),(bx,by))))
    return xmin, xmax


class ProblemInput(NamedTuple):
    filename: str
    test_y: int
    max_coord: int
    part_1: int = None
    part_2: int = None

EXAMPLE = ProblemInput(filename='./test.txt',test_y=10,max_coord=20,part_1=26,part_2=56000011)
PROBLEM = ProblemInput(filename='./input.txt',test_y= 2000000,max_coord=4000000, part_1=4717631)

def part_1(input):
    xmin, xmax = parse_input(input.filename)
    test_y = input.test_y
    ignored_cols = set()
    no_beacons = set()
    for b in BEACONS:
        if b[1] == test_y:
            ignored_cols.add(b[0])
    for s in SENSORS:
        if s.y == test_y:
            ignored_cols.add(s.x)
    for i,s in enumerate(SENSORS):
        dist_to_y = abs(s.y-test_y)
        if dist_to_y >= s.m:
            continue
        m = s.m - dist_to_y
        for i in range(0,m+1):
            no_beacons.add(s.x+i)
            no_beacons.add(s.x-i)
    no_beacons -= ignored_cols
    ans = len(no_beacons)
    if input.part_1:
        assert ans==input.part_1
    print(ans)


def consolidate_segment_list(sl):
    consolidated = []
    cur = [sl[0][0],sl[0][1]]
    # print(sl)
    for i in range(1,len(sl)):
        s= sl[i]
        # print(f"s = {s}")
        if s[0] > cur[1]+1:
            consolidated.append(cur)
            cur = [s[0],s[1]]
        else:
            cur[0] = min(s[0],cur[0])
            cur[1] = max(s[1],cur[1])
        # print(f"cur = {cur}")
        # print(f"consolidated = {consolidated}")

    if cur:
        consolidated.append(cur)
    return consolidated

def part_2(input: ProblemInput):
    # Test answer x=14, y=11, tuning frequency = 56000011
    xmin, xmax = parse_input(input.filename)
    coord_max = input.max_coord
    ignored_cols = set()
    no_beacons = set()
    # Sort sensors by x so we can scan left to right
    sorted_sensors = sorted(SENSORS,key=lambda s: s.x)
    for y in range(0,coord_max+1):
        if y % 10000 == 0:
            print(f"{y}...")
        no_beacon_segments = []
        for s in sorted_sensors:
            nbs = s.no_beacon_segment(y)
            if nbs:
                no_beacon_segments.append(nbs)
        consolidated = True
        while consolidated:
            len_nbs = len(no_beacon_segments)
            no_beacon_segments = consolidate_segment_list(no_beacon_segments)
            if len(no_beacon_segments) == len_nbs:
                consolidated = False
        if len(no_beacon_segments) == 2:
            x = no_beacon_segments[0][1]+1
            print(f"({x},{y})")
            ans = 4000000*x+y
            print(ans)
            if input.part_2:
                assert ans == input.part_2
            return
    assert False

print("PART 1:")
# part_1(EXAMPLE)
# part_1(PROBLEM)

print("PART 2:")
# part_2(EXAMPLE)
part_2(PROBLEM)