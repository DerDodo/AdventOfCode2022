from typing import List, Tuple, Dict

from util.file_util import read_input_file

Robots = Dict[str, int]

ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"

ALL_MATERIALS = [ORE, CLAY, OBSIDIAN, GEODE]


class Materials:
    items: Dict[str, int]

    def __init__(self, materials: Dict[str, int]):
        self.items = materials.copy()
        for material in ALL_MATERIALS:
            if material not in self.items: self.items[material] = 0

    def is_contained_in(self, other):
        for material in ALL_MATERIALS:
            if self.items[material] > other.items[material]:
                return False
        return True

    def decrease(self, other):
        if not other.is_contained_in(self):
            raise ValueError("Cannot decrease materials")

        for material in ALL_MATERIALS:
            self.items[material] -= other.items[material]

    def add(self, other):
        for material in ALL_MATERIALS:
            self.items[material] += other.items[material]

    def has_any(self, materials: List[str]) -> bool:
        for material in materials:
            if self.items[material] > 0:
                return True
        return False

    def get_max(self) -> Tuple[List[str], int]:
        max_material = max(self.items.values())
        return [material for material in self.items if self.items[material] == max_material], max_material


class Blueprint:
    id: int
    robot_cost: Dict[str, Materials]
    max_robots_needed: Dict[str, int]

    def __init__(self, line: str):
        parts = line.split(" ")
        self.id = int(parts[1].replace(":", ""))
        self.robot_cost = {
            ORE: Materials({ORE: int(parts[6])}),
            CLAY: Materials({ORE: int(parts[12])}),
            OBSIDIAN: Materials({ORE: int(parts[18]), CLAY: int(parts[21])}),
            GEODE: Materials({ORE: int(parts[27]), OBSIDIAN: int(parts[30])}),
        }
        self.max_robots_needed = {}
        for material in ALL_MATERIALS:
            self.max_robots_needed[material] =

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
            materials.items[material] += robots[material]
        if new_robot is not None:
            blueprint.consume_resources(new_robot, materials)
            robots[new_robot] += 1
    return materials.items[GEODE]


def calc_best_num_geodes(blueprint: Blueprint) -> int:
    return max(
        mine(blueprint, strategy_prefer_later),
        mine(blueprint, strategy_2_by_2),
    )


class State:
    minute: int
    robots: Robots
    materials: Materials

    def __init__(self, minute: int, robots: Robots, materials: Materials):
        self.minute = minute
        self.robots = robots
        self.materials = materials

    def num_geodes(self) -> int:
        return self.materials.items[GEODE]

    def should_build(self, blueprint: Blueprint, robot: str) -> bool:
        return self.robots[robot] <


def max_for_blueprint(blueprint: Blueprint):
    states: List[List[State]] = [[]]
    states[0].append(State(0, {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}, Materials({})))
    max_geodes = 0

    for minute in range(24):
        states.append([])
        for state in states[minute]:
            if state.num_geodes() >= max_geodes - 2:
                new_state = create_new_state(blueprint, state, None)
                states[minute + 1].append(new_state)
                max_geodes = max(max_geodes, new_state.num_geodes())
                for material in ALL_MATERIALS:
                    if blueprint.can_build(material, state.materials) and state.should_build(blueprint, material):
                        new_state = create_new_state(blueprint, state, material)
                        states[minute + 1].append(new_state)
                        max_geodes = max(max_geodes, new_state.num_geodes())

    for state in states[24]:
        max_geodes = max(max_geodes, state.num_geodes())

    return max_geodes


def create_new_state(blueprint: Blueprint, seed_state: State, action: str | None) -> State:
    materials = Materials(seed_state.materials.items)
    robots = seed_state.robots.copy()

    for material in ALL_MATERIALS:
        materials.items[material] += seed_state.robots[material]
    if action is not None:
        blueprint.consume_resources(action, materials)
        robots[action] += 1

    return State(seed_state.minute + 1, robots, materials)


def level19() -> Tuple[int, int]:
    blueprints = parse_input_file()
    sum_quality = 0
    for blueprint in blueprints:
        num_geodes = max_for_blueprint(blueprint)
        sum_quality += blueprint.id * num_geodes
    return sum_quality, 0


if __name__ == "__main__":
    _sum_quality, _num = level19()
    print(f"Quality sum: {_sum_quality}")
