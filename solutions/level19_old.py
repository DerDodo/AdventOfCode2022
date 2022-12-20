from typing import List, Set, Tuple, Dict

from util.file_util import read_input_file

Robots = Dict[str, int]

ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"

ALL_MATERIALS = [ORE, CLAY, OBSIDIAN, GEODE]


class Materials:
    materials: Dict[str, int]

    def __init__(self, materials: Dict[str, int]):
        self.materials = materials.copy()
        for material in ALL_MATERIALS:
            if material not in self.materials: self.materials[material] = 0

    def is_contained_in(self, other):
        for material in ALL_MATERIALS:
            if self.materials[material] > other.materials[material]:
                return False
        return True

    def decrease(self, other):
        if not other.is_contained_in(self):
            raise ValueError("Cannot decrease materials")

        for material in ALL_MATERIALS:
            self.materials[material] -= other.materials[material]

    def add(self, other):
        for material in ALL_MATERIALS:
            self.materials[material] += other.materials[material]

    def has_any(self, materials: List[str]) -> bool:
        for material in materials:
            if self.materials[material] > 0:
                return True
        return False

    def get_max(self) -> Tuple[List[str], int]:
        max_material = max(self.materials.values())
        return [material for material in self.materials if self.materials[material] == max_material], max_material


class Blueprint:
    id: int
    robot_cost: Dict[str, Materials]

    def __init__(self, line: str):
        parts = line.split(" ")
        self.id = int(parts[1].replace(":", ""))
        self.robot_cost = {
            ORE: Materials({ORE: int(parts[6])}),
            CLAY: Materials({ORE: int(parts[12])}),
            OBSIDIAN: Materials({ORE: int(parts[18]), CLAY: int(parts[21])}),
            GEODE: Materials({ORE: int(parts[27]), OBSIDIAN: int(parts[30])}),
        }

    def can_build(self, robot: str, materials: Materials) -> bool:
        return self.robot_cost[robot].is_contained_in(materials)

    def consume_resources(self, robot: str, materials: Materials):
        materials.decrease(self.robot_cost[robot])


def parse_input_file() -> List[Blueprint]:
    lines = read_input_file(19)
    return list(map(Blueprint, lines))


def strategy_prefer_later(blueprint: Blueprint, materials: Materials, _: Robots) -> str | None:
    for robot_type in [GEODE, OBSIDIAN, CLAY, ORE]:
        if blueprint.can_build(robot_type, materials):
            return robot_type
    return None


def strategy_calc_resource_need(blueprint: Blueprint, materials: Materials, robots: Robots) -> str | None:
    if blueprint.can_build(GEODE, materials):
        return GEODE

    needed_materials = Materials({
        ORE: 0,
        CLAY: 0,
        OBSIDIAN: 0,
        GEODE: 0,
    })
    needed_materials.add(blueprint.robot_cost[GEODE])
    materials_served_by_robots = [material for material in ALL_MATERIALS if material in robots]

    most_needed_materials, num_needed = needed_materials.get_max()
    most_needed_materials.reverse()
    for most_needed_material in most_needed_materials:
        if blueprint.can_build(most_needed_material, materials):
            return most_needed_material
        needed_materials.add(blueprint.robot_cost[most_needed_material])


def strategy_2_by_2(blueprint: Blueprint, materials: Materials, robots: Robots) -> str | None:
    num_robots = sum(robots.values())
    robot = ALL_MATERIALS[(num_robots // 2) % 4]
    if blueprint.can_build(robot, materials):
        return robot
    return None


def mine(blueprint: Blueprint, strategy) -> int:
    materials = Materials({})
    robots = {
        ORE: 1,
        CLAY: 0,
        OBSIDIAN: 0,
        GEODE: 0,
    }
    for _ in range(24):
        new_robot = strategy(blueprint, materials, robots)
        for material in ALL_MATERIALS:
            materials.materials[material] += robots[material]
        if new_robot is not None:
            blueprint.consume_resources(new_robot, materials)
            robots[new_robot] += 1
    return materials.materials[GEODE]


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
