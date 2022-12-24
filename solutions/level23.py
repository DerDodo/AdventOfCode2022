from collections import defaultdict
from enum import Enum
from typing import List, Tuple, Dict, Any

from util.file_util import read_input_file


POSITION_ID_KEY = 10000


class Direction(Enum):
    North = 0
    South = 1
    West = 2
    East = 3


def get_position_id(x: int, y: int) -> int:
    return x + y * POSITION_ID_KEY


def get_coordinates(position_id: int) -> Tuple[int, int]:
    y = position_id // POSITION_ID_KEY
    x = position_id - y * POSITION_ID_KEY
    return x, y


class Elf:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_position_id(self) -> int:
        return get_position_id(self.x, self.y)

    def get_movement_proposal(
        self, elves: Dict[int, Any], direction_check_order: List[Direction]
    ) -> Tuple[int | None, int | None]:
        nw_free = get_position_id(self.x - 1, self.y - 1) not in elves
        n_free = get_position_id(self.x, self.y - 1) not in elves
        ne_free = get_position_id(self.x + 1, self.y - 1) not in elves
        w_free = get_position_id(self.x - 1, self.y) not in elves
        e_free = get_position_id(self.x + 1, self.y) not in elves
        sw_free = get_position_id(self.x - 1, self.y + 1) not in elves
        s_free = get_position_id(self.x, self.y + 1) not in elves
        se_free = get_position_id(self.x + 1, self.y + 1) not in elves

        if nw_free and n_free and ne_free and w_free and e_free and sw_free and s_free and se_free:
            return None, None

        move_north = nw_free and n_free and ne_free
        move_south = sw_free and s_free and se_free
        move_west = w_free and nw_free and sw_free
        move_east = e_free and ne_free and se_free

        return self._propose_movement(direction_check_order, move_north, move_south, move_west, move_east)

    def _propose_movement(
        self,
        direction_check_order: List[Direction],
        move_north: bool,
        move_south: bool,
        move_west: bool,
        move_east: bool,
    ) -> Tuple[int, int]:
        for direction in direction_check_order:
            if direction == Direction.North and move_north:
                return self.x, self.y - 1
            elif direction == Direction.South and move_south:
                return self.x, self.y + 1
            elif direction == Direction.West and move_west:
                return self.x - 1, self.y
            elif direction == Direction.East and move_east:
                return self.x + 1, self.y

        return self.x, self.y


Elves = Dict[int, Elf]
MovementProposal = Dict[int, List[Elf]]


def parse_input_file() -> Elves:
    lines = read_input_file(23)
    elves: Elves = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                elf = Elf(x + POSITION_ID_KEY // 2, y + POSITION_ID_KEY // 2)
                elves[elf.get_position_id()] = elf
    return elves


def get_covered_area_dimensions(elves: Elves) -> Tuple[int, int, int, int]:
    min_x, min_y, max_x, max_y = 100000, 100000, -1000000, -1000000
    for elf in elves.values():
        min_x = min(min_x, elf.x)
        max_x = max(max_x, elf.x)
        min_y = min(min_y, elf.y)
        max_y = max(max_y, elf.y)
    return min_x, max_x, min_y, max_y


def get_covered_area(elves: Elves) -> int:
    min_x, max_x, min_y, max_y = get_covered_area_dimensions(elves)
    len_x = max_x - min_x + 1
    len_y = max_y - min_y + 1
    return len_x * len_y - len(elves)


def print_area(elves: Elves):
    min_x, max_x, min_y, max_y = get_covered_area_dimensions(elves)
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            line += "#" if get_position_id(x, y) in elves else "."
        print(line)


def propose_movements(elves: Elves, direction_check_order: List[Direction]) -> [MovementProposal, List[Elf]]:
    movement_proposals: MovementProposal = defaultdict(list)
    not_moved_elves = []
    for elf in elves.values():
        x, y = elf.get_movement_proposal(elves, direction_check_order)
        if x is None:
            not_moved_elves.append(elf)
        else:
            movement_proposals[get_position_id(x, y)].append(elf)
    return movement_proposals, not_moved_elves


def move_elves(elves: Elves, direction_check_order: List[Direction]) -> Tuple[Elves, bool]:
    movement_proposals, not_moved_elves = propose_movements(elves, direction_check_order)
    new_elves: Elves = {}

    for movement_proposal_id in movement_proposals:
        movement_proposal = movement_proposals[movement_proposal_id]
        if len(movement_proposal) == 1:
            elf = movement_proposal[0]
            new_elves[movement_proposal_id] = elf
            x, y = get_coordinates(movement_proposal_id)
            elf.x = x
            elf.y = y
        else:
            for elf in movement_proposal:
                new_elves[elf.get_position_id()] = elf

    for elf in not_moved_elves:
        new_elves[elf.get_position_id()] = elf

    return new_elves, len(movement_proposals) == 0


def level23() -> Tuple[int, int]:
    elves = parse_input_file()
    round_10_result = -1
    direction_check_order = [
        Direction.North,
        Direction.South,
        Direction.West,
        Direction.East,
    ]

    for i in range(5000):
        if i > 50 and i % 100 == 0:
            print(f"Iteration {i}", flush=True)

        elves, finished = move_elves(elves, direction_check_order)
        direction_check_order.append(direction_check_order.pop(0))

        if i == 9:
            round_10_result = get_covered_area(elves)

        if finished:
            return round_10_result, i + 1

    raise ValueError("Couldn't find result in 5000 iterations")


if __name__ == "__main__":
    _covered_area, _final_round = level23()
    print(f"Covered area: {_covered_area}")
    print(f"Final round: {_final_round}")
