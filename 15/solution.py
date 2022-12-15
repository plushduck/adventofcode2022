import re

BEACONS = []
SENSORS = []

def manhattan(t1,t2):
    return(abs(t1[0]-t2[0]) + abs(t1[1]-t2[1]))

def parse_input(filename):
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
        mmax = 0
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
            mmax = max(mmax,manhattan((bx,by),(sx,sy)))
            BEACONS.append((bx,by))
            SENSORS.append((sx,sy))

    return xmin, xmax, mmax

def part_1():
    xmin, xmax, mmax = parse_input('./test.txt')
    test_x = 11
    ignored_cols = set()
    no_beacons = set()
    for b in BEACONS:
        if b[1] == test_x:
            ignored_cols.add(b[0])
    for s in SENSORS:
        if s[1] == test_x:
            ignored_cols.add(s[0])
    for i,sensor in enumerate(SENSORS):
        m = manhattan(sensor, BEACONS[i])
        dist_to_x = abs(sensor[1]-test_x)
        if dist_to_x >= m:
            continue
        m -= dist_to_x

        sx = sensor[0]
        for i in range(0,m+1):
            no_beacons.add(sx+i)
            no_beacons.add(sx-i)
    no_beacons -= ignored_cols
    print(no_beacons)
    print(len(no_beacons))

# Test answer = 4717631
# part_1()

def part_2():
    # Test answer x=14, y=11, tuning frequency = 56000011
    xmin, xmax, mmax = parse_input('./input.txt')
    coord_max = 4000000
    ignored_cols = set()
    no_beacons = set()
    sorted_sensors = sorted(list(set(SENSORS)),key=lambda b: b[1])
    ignored_lines = set()
    for i,s in enumerate(SENSORS):
        b = BEACONS[i]
        m = manhattan(s,b)
        dist_to_0 = abs(s[0])
        dist_to_max = abs(s[0]-coord_max)
        overshoot = m - max(dist_to_0,dist_to_max)
        print(f"{s}/{b}: manhattan {m}, overshoot {overshoot}")
        if overshoot > 0:
            for i in range(0,overshoot+1):
                ignored_lines.add(s[1]+i)
                ignored_lines.add(s[1]-i)

    print(len(ignored_lines))

part_2()