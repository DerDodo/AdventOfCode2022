from collections import deque
from random import shuffle
from typing import List, Dict, Set, Deque

from util.file_util import read_input_file


class Valve:
    id: str
    flow_rate: int
    connected_rooms: List[str]

    def __init__(self, definition: str):
        parts = definition.split(" ")
        self.id = parts[1]
        self.flow_rate = int(parts[4][5:-1])
        connection_str = " ".join(definition.split(" valve")[1].split(" ")[1:])
        self.connected_rooms = connection_str.split(", ")


def parse_input_file() -> Dict[str, Valve]:
    lines = read_input_file(16)
    valves = map(Valve, lines)
    return {valve.id: valve for valve in valves}


def generate_all_permutations(item: List[str]) -> List[List[str]]:
    if len(item) == 0:
        return []

    if len(item) == 1:
        return [item]

    permutations = []
    for i in range(len(item)):
        start = item[i]
        remaining_list = item[:i] + item[i + 1 :]
        for permutation in generate_all_permutations(remaining_list):
            permutations.append([start] + permutation)
    return permutations


# https://onestepcode.com/graph-shortest-path-python/
def shortest_path(graph: Dict[str, Valve], start, end) -> Deque[str]:
    path_list: List[Deque[str]] = [[start]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes: Set[str] = {start}
    if start == end:
        return path_list[0]

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = graph[last_node].connected_rooms
        # Search goal node
        if end in next_nodes:
            current_path.append(end)
            return current_path[1:]
        # Add new paths
        for next_node in next_nodes:
            if next_node not in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return deque()


def find_steps(graph: Dict[str, Valve], route: List[str]) -> Deque[str]:
    steps: Deque[str] = deque()
    for i in range(len(route) - 1):
        steps.extend(shortest_path(graph, route[i], route[i + 1]))
    return steps


def level16_2(targets_start: list[str], elephant_targets_start: list[str]) -> int:
    valves = parse_input_file()
    all_targets = list(filter(lambda valve: valves[valve].flow_rate > 0, valves))
    reduced_targets = [target for target in all_targets if target not in targets_start]
    reduced_targets = [target for target in reduced_targets if target not in elephant_targets_start]
    max_pressure = 0
    for _ in range(100000):
        shuffle(reduced_targets)
        targets = targets_start + reduced_targets
        shuffle(reduced_targets)
        elephant_targets = elephant_targets_start + reduced_targets

        next_target = 0
        elephant_next_target = 0
        steps = find_steps(valves, ["AA"] + targets)
        elephant_steps = find_steps(valves, ["AA"] + elephant_targets)
        current_room = "AA"
        elephant_current_room = "AA"

        valves_opened: Set[str] = set()
        pressure_release_per_minute = 0
        pressure_released = 0
        for _ in range(26):
            pressure_released += pressure_release_per_minute

            if (
                valves[current_room].flow_rate > 0
                and len(targets) > next_target
                and current_room == targets[next_target]
                and current_room not in valves_opened
            ):
                pressure_release_per_minute += valves[current_room].flow_rate
                valves_opened.add(current_room)
                next_target += 1
            elif len(steps) > 0:
                current_room = steps.popleft()

            if (
                valves[elephant_current_room].flow_rate > 0
                and len(elephant_targets) > elephant_next_target
                and elephant_current_room == elephant_targets[elephant_next_target]
                and elephant_current_room not in valves_opened
            ):
                pressure_release_per_minute += valves[elephant_current_room].flow_rate
                valves_opened.add(elephant_current_room)
                elephant_next_target += 1
            elif len(elephant_steps) > 0:
                elephant_current_room = elephant_steps.popleft()

        if max_pressure < pressure_released:
            print(f"New best route! pressure: {pressure_released}", flush=True)
            print(f"route: {' -> '.join(targets)}", flush=True)
            print(f"eleph: {' -> '.join(elephant_targets)}", flush=True)
            max_pressure = pressure_released

    return max_pressure


if __name__ == "__main__":
    # _max_pressure = level16_2([], [])
    # _max_pressure = level16_2(["EX"], ["TA"])  # 2165
    # _max_pressure = level16_2(["QK"], ["TA"])  # 2389
    # _max_pressure = level16_2(["QK", "JA"], ["TA", "DC"])  # 2461
    # _max_pressure = level16_2(["QK", "JA", "VK"], ["TA", "DC", "XN"])  # 2610
    _max_pressure = level16_2(["QK", "JA", "VK", "ID"], ["TA", "DC", "XN", "DH"])  # 2675
    print(f"Max pressure: {_max_pressure}")
