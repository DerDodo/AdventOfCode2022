from typing import List, Tuple, Dict

from util.file_util import read_input_file

Robots = Dict[str, int]

ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"

ALL_MATERIALS = [ORE, CLAY, OBSIDIAN, GEODE]
ALL_BUT_GEODE = [ORE, CLAY, OBSIDIAN]


class Materials:
    items: Dict[str, int]

    def __init__(self, materials: Dict[str, int]):
        self.items = materials.copy()
        for material in ALL_MATERIALS:
            if material not in self.items:
                self.items[material] = 0

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
        for material in ALL_BUT_GEODE:
            self.max_robots_needed[material] = max(map(lambda cost: cost.items[material], self.robot_cost.values()))
        self.max_robots_needed[GEODE] = 1000

    def can_build(self, robot: str, materials: Materials) -> bool:
        return self.robot_cost[robot].is_contained_in(materials)

    def consume_resources(self, robot: str, materials: Materials):
        materials.decrease(self.robot_cost[robot])


def parse_input_file() -> List[Blueprint]:
    lines = read_input_file(19)
    return list(map(Blueprint, lines))


class State:
    minute: int
    robots: Robots
    materials: Materials
    target_robot: str

    def __init__(self, minute: int, robots: Robots, materials: Materials, target_robot: str):
        self.minute = minute
        self.robots = robots
        self.materials = materials
        self.target_robot = target_robot

    def num_geodes(self) -> int:
        return self.materials.items[GEODE]

    def can_build_any_new_bot(self, blueprint: Blueprint) -> bool:
        for robot in self.robots:
            if self.robots[robot] == 0 and blueprint.can_build(robot, self.materials):
                return True
        return False

    def can_build_target(self, blueprint: Blueprint) -> bool:
        return blueprint.can_build(self.target_robot, self.materials)


def can_build_when_waiting(robots: Robots, robot: str):
    if robot == ORE or robot == CLAY:
        return True
    elif robot == OBSIDIAN:
        return robots[CLAY] > 0
    elif robot == GEODE:
        return robots[OBSIDIAN] > 0


def should_build(blueprint: Blueprint, robots: Robots, robot: str) -> bool:
    return robots[robot] < blueprint.max_robots_needed[robot]


def get_max_geodes(states: List[State]) -> bool:
    max_geodes = 0
    for state in states:
        max_geodes = max(max_geodes, state.num_geodes())
    return max_geodes


def max_for_blueprint(blueprint: Blueprint, minutes: int):
    states: List[List[State]] = [[]]
    states[0].append(State(0, {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}, Materials({}), ORE))
    states[0].append(State(0, {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}, Materials({}), CLAY))
    max_geode_bots = 0

    for minute in range(minutes):
        states.append([])
        for state in states[minute]:
            new_states = create_next_states(state, blueprint)
            for new_state in new_states:
                if new_state.robots[GEODE] >= max_geode_bots or new_state.target_robot == GEODE:
                    max_geode_bots = max(max_geode_bots, new_state.robots[GEODE])
                    states[minute + 1].append(new_state)

    max_geodes = get_max_geodes(states[minutes])

    return max_geodes


def create_next_states(state: State, blueprint: Blueprint) -> List[State]:
    if state.can_build_target(blueprint):
        return build(blueprint, state)
    else:
        return [wait(state)]


def wait(seed_state: State) -> State:
    materials = Materials(seed_state.materials.items)
    robots = seed_state.robots.copy()

    for material in ALL_MATERIALS:
        materials.items[material] += seed_state.robots[material]

    return State(seed_state.minute + 1, robots, materials, seed_state.target_robot)


def build(blueprint: Blueprint, seed_state: State) -> List[State]:
    materials = Materials(seed_state.materials.items)
    robots = seed_state.robots.copy()

    for material in ALL_MATERIALS:
        materials.items[material] += seed_state.robots[material]

    blueprint.consume_resources(seed_state.target_robot, materials)
    robots[seed_state.target_robot] += 1

    new_states = []
    for material in ALL_MATERIALS:
        if can_build_when_waiting(robots, material) and should_build(blueprint, robots, material):
            new_states.append(State(seed_state.minute + 1, robots, materials, material))
    return new_states


def level19_part(minutes: int, blueprints: List[Blueprint]) -> Tuple[int, int]:
    sum_quality = 0
    geode_product = 1
    for blueprint in blueprints:
        num_geodes = max_for_blueprint(blueprint, minutes)
        sum_quality += blueprint.id * num_geodes
        geode_product *= num_geodes
    return sum_quality, geode_product


def level19() -> Tuple[int, int]:
    blueprints = parse_input_file()
    return level19_part(24, blueprints)[0], level19_part(32, blueprints[0:3])[1]


if __name__ == "__main__":
    _sum_quality_1, _geode_product_2 = level19()
    print(f"Quality sum (1): {_sum_quality_1}")
    print(f"Geode product (2): {_geode_product_2}")
