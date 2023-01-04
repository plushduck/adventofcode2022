import re

from copy import copy
from dataclasses import dataclass
from itertools import combinations
from typing import Set

valve_re = r'Valve (?P<name>[A-Z]+)'
flow_re = r' has flow rate=(?P<flow>\d+)'
adjacent_re = r'; tunnels? leads? to valves? (?P<adjacent>[A-Z, ]+)'
re_str = valve_re+flow_re+adjacent_re
valve_parser = re.compile(valve_re+flow_re+adjacent_re)

@dataclass
class Valve:
    name: str
    flow: int
    adjacent: Set[str]

def parse_valves(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        valves = {}
        for l in lines:
            m = valve_parser.match(l)
            name = m.group('name')
            flow = int(m.group('flow'))
            adjacent = m.group('adjacent')
            adjacent = adjacent.replace(" ", "")
            adjacent = set(adjacent.split(','))
            valves[name] = Valve(name, flow, adjacent)
        return valves

# Calculate the distances between any two nodes
def get_distances(valves):
    distances = {}
    for v in valves.values():
        distance = 1
        visited = set()
        visited.add(v.name)
        next_visits = set()
        next_visits.update(v.adjacent)
        while(next_visits):
            to_visit = set()
            for dest_name in next_visits:
                visited.add(dest_name)
                to_visit.update(valves[dest_name].adjacent)
                distances[frozenset((v.name, dest_name))] = distance
            to_visit -= visited
            next_visits = to_visit
            distance += 1
    return distances


def get_optimal_flow(valves, distances):

    # We only need to consider the visit order to nodes with flow valves
    flow_valves = [v.name for v in valves.values() if v.flow]

    # The max possible flow occurs when all valves are open.
    max_possible_flow = 0
    for name in flow_valves:
        max_possible_flow += valves[name].flow

    # Do a depth first search
    best_path = None
    best_flow = 0
    # Represents nodes that still need to be considered in this position, in a depth first sense.
    search_nodes = [set(flow_valves)]
    path_time = [0]
    path_flow_total = [0]
    path_flow_rate = [0]
    path = []
    while(search_nodes):

        prev_node = 'AA' if len(search_nodes) == 1 else path[-1]

#         print(f"prev_node = {prev_node}")
#        print(f"search_nodes = {search_nodes}")
        # print(f"path_time = {path_time}")
        # print(f"path_flow_total = {path_flow_total}")
        # print(f"path_flow_rate = {path_flow_rate}")
#        print(f"path = {path}")

        # Select the next node:
        cur_node = search_nodes[-1].pop()

        # print(f"cur_node = {cur_node}")
        path.append(cur_node)
        search_nodes.append(set(flow_valves) - set(path))
            # search_nodes.append(copy(search_nodes[-1]))
        # print(f"new search_nodes = {search_nodes}")
        # print(f"{path}")

        # We'll stay at the current flow rate until we reach a new node or
        # the max number of steps has been reached.
        step_time = distances[frozenset((prev_node,cur_node))]
        step_time = min(step_time, 30 - path_time[-1])
        path_time.append(step_time+path_time[-1])
        # print(f"path_time = {path_time}")

        # Track flow during step
        step_flow = step_time * path_flow_rate[-1]
        path_flow_total.append(step_flow + path_flow_total[-1])
        path_flow_rate.append(path_flow_rate[-1])

        # Open the cur node's valve if there's time
        if path_time[-1] < 30:
            path_time[-1] += 1
            path_flow_total[-1] += path_flow_rate[-1]
            path_flow_rate[-1]+=valves[cur_node].flow

        # Run out the time if the path contains all nodes
        if len(path) == len(flow_valves) and path_time[-1] < 30:
            step_time = 30 - path_time[-1]
            path_time[-1] = 30
            step_flow = step_time * path_flow_rate[-1]
            path_flow_total[-1] += step_flow
            print(f"path_flow_total = {path_flow_total}")
            print(f"path_flow_rate = {path_flow_rate}")

        # Maybe update best path
        if path_time[-1] == 30 and path_flow_total[-1] > best_flow:
            best_path = copy(path)
            best_flow = path_flow_total[-1]
            print(f"NEW BEST ({best_flow}) {path}")

        time_remaining = 30 - path_time[-1]
        max_flow_remaining = time_remaining * max_possible_flow
        max_path_flow_total = max_flow_remaining + path_flow_total[-1]

        if not search_nodes[-1]:
            assert path_time[-1] == 30

        # Unwind the search path if any of the following are true:
        # * There are no more paths to search with the currently-constructed path prefix
        # * We've hit the max number of steps along the current path
        # * The max possible total flow along the current path is less than the best path already discovered
        while search_nodes and (len(search_nodes[-1]) <= 0 or path_time[-1] == 30 or max_path_flow_total < best_flow) :
            # print("POPPING")
            search_nodes.pop()
            if path:
                path.pop()
                path_time.pop()
                path_flow_total.pop()
                path_flow_rate.pop()
            time_remaining = 30 - path_time[-1]
            max_flow_remaining = time_remaining * max_possible_flow
            max_path_flow_total = max_flow_remaining + path_flow_total[-1]
            # print(f"popped search_nodes = {search_nodes}")
            # print(f"popped path = {path}")

    print(f"best_path = {best_path}")
    print(f"best_flow = {best_flow}")
    print(f"max_possible_flow = {max_possible_flow}")
    return best_flow

def part_1(filename):
    print("PART 1")
    valves = parse_valves(filename)
    distances = get_distances(valves)
    return get_optimal_flow(valves, distances)

p1_ans = part_1('./input.txt')
assert p1_ans == 1796