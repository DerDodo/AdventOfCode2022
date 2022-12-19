from enum import Enum
from typing import List, Set, Tuple, Dict

from util.file_util import read_input_file


Materials = Dict[str, int]
Robots = Dict[str, int]


ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"

ALL_MATERIALS = [ORE, CLAY, OBSIDIAN, GEODE]


class Blueprint:
    id: int
    robot_cost: Dict[str, Dict[str, int]]

    def __init__(self, line: str):
        parts = line.split(" ")
        self.id = int(parts[1].replace(":", ""))
        self.robot_cost = {
            ORE: {ORE: int(parts[6])},
            CLAY: {ORE: int(parts[12])},
            OBSIDIAN: {ORE: int(parts[18]), CLAY: int(parts[21])},
            GEODE: {ORE: int(parts[27]), OBSIDIAN: int(parts[30])},
        }

    def can_build(self, robot: str, materials: Materials) -> bool:
        for cost in self.robot_cost[robot]:
            if materials[cost] < self.robot_cost[robot][cost]:
                return False
        return True

    def consume_resources(self, robot: str, materials: Materials):
        for cost in self.robot_cost[robot]:
            if materials[cost] < self.robot_cost[robot][cost]:
                raise ValueError(f"Cannot consume resources! blueprint: {self.id}, robot: {robot}, material: {cost}, available: {materials[cost]}, needed: {self.robot_cost[robot][cost]}")
            materials[cost] -= self.robot_cost[robot][cost]


def parse_input_file() -> List[Blueprint]:
    lines = read_input_file(19)
    return list(map(Blueprint, lines))


def strategy_prefer_later(blueprint: Blueprint, materials: Materials, _: Robots) -> str | None:
    for robot_type in [GEODE, OBSIDIAN, CLAY, ORE]:
        if blueprint.can_build(robot_type, materials):
            return robot_type
    return None


def strategy_calc_resource_need(blueprint: Blueprint, materials: Materials, _: Robots) -> str | None:
    need = {
        ORE: 0,
        CLAY: 0,
        OBSIDIAN: 0,
        GEODE: 0,
    }

    if blueprint.can_build(GEODE, materials):
        return GEODE

    for cost in blueprint.robot_cost[GEODE]:
        need[cost] += blueprint.robot_cost[GEODE][cost]

    temp_max = max(need.values())
    most_needed_materials = [key for key in need if need[key] == temp_max]
    for material in most_needed_materials:
        if blueprint.can_build(material, materials):
            return material

    go_on = True
    while go_on:
        for material in ALL_MATERIALS:
            need[material]


def strategy_2_by_2(blueprint: Blueprint, materials: Materials, robots: Robots) -> str | None:
    num_robots = sum(robots.values())
    robot = ALL_MATERIALS[(num_robots // 2) % 4]
    if blueprint.can_build(robot, materials):
        return robot
    return None


def mine(blueprint: Blueprint, strategy) -> int:
    materials = {
        ORE: 0,
        CLAY: 0,
        OBSIDIAN: 0,
        GEODE: 0,
    }
    robots = {
        ORE: 1,
        CLAY: 0,
        OBSIDIAN: 0,
        GEODE: 0,
    }
    for _ in range(24):
        new_robot = strategy(blueprint, materials, robots)
        for material in ALL_MATERIALS:
            materials[material] += robots[material]
        if new_robot is not None:
            blueprint.consume_resources(new_robot, materials)
            robots[new_robot] += 1
    return materials[GEODE]


def calc_best_num_geodes(blueprint: Blueprint) -> int:
    return max(
        mine(blueprint, strategy_prefer_later),
        mine(blueprint, strategy_2_by_2),
    )


def level19() -> Tuple[int, int]:
    blueprints = parse_input_file()
    sum_quality = 0
    for blueprint in blueprints:
        geodes = calc_best_num_geodes(blueprint)
        sum_quality += geodes * blueprint.id
        print(f"Blueprint {blueprint.id}: {geodes} geodes")
    return sum_quality, 0


if __name__ == "__main__":
    _sum_quality, _num = level19()
    print(f"Quality sum: {_sum_quality}")
