from math import ceil
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
            if material not in self.items:
                self.items[material] = 0

    def is_contained_in(self, other):
        for material in ALL_MATERIALS:
            if self.items[material] > other.items[material]:
                return False
        return True

    def decrease(self, other):
        for material in ALL_MATERIALS:
            self.items[material] = max(0, self.items[material] - other.items[material])

    def add(self, other):
        for material in ALL_MATERIALS:
            self.items[material] += other.items[material]

    def mul_add(self, robots: Robots, mul: int):
        for material in ALL_MATERIALS:
            self.items[material] += robots[material] * mul

    def divide_ceil(self, robots: Robots):
        for material in ALL_MATERIALS:
            if robots[material] > 0:
                self.items[material] = ceil(self.items[material] / robots[material])
            elif self.items[material] != 0:
                self.items[material] = 100000000


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


class WaitAndBuild:
    robot: str
    wait_for: Materials

    def __init__(self, robot: str, cost: Materials):
        self.robot = robot
        self.wait_for = Materials(cost.items)

    def get_wait_time(self, inventory: Materials, robots: Robots) -> Tuple[int, str]:
        time = Materials(self.wait_for.items)
        time.decrease(inventory)
        time.divide_ceil(robots)
        max_time = max(time.items.values())
        resources = [material for material in time.items if time.items[material] == max_time]
        min_robots = min([robots[robot] for robot in robots if robot in resources])
        resource = [robot for robot in robots if robots[robot] == min_robots and robot in resources]
        return max_time, resource[-1]


class Strategy:
    steps: List[WaitAndBuild]
    blueprint: Blueprint

    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint
        self.steps = []
        self.add_step(CLAY, 0)
        self.add_step(OBSIDIAN, 1)
        self.add_step(GEODE, 2)
        self.optimize()
        while self.get_total_time() < 24:
            self.add_step(GEODE, len(self.steps))
            self.optimize()

    def add_step(self, robot: str, position: int):
        self.steps.insert(position, WaitAndBuild(robot, self.blueprint.robot_cost[robot]))

    def add_steps(self, robots: List[str], position: int):
        steps = [WaitAndBuild(robot, self.blueprint.robot_cost[robot]) for robot in robots]
        steps.reverse()
        for step in steps:
            self.steps.insert(position, step)

    def _calc_optimization_priority(self) -> List[Tuple[int, Tuple[int, str]]]:
        wait_times = self.get_wait_times(self.steps)

        priority: List[Tuple[int, Tuple[int, str]]] = []
        for i in range(len(wait_times)):
            priority.append((i, wait_times[i]))
        priority.sort(key=lambda p: p[1][0], reverse=True)

        return priority

    def optimize(self):
        last_num_steps = 0
        priority = self._calc_optimization_priority()

        while last_num_steps != len(self.steps):
            last_num_steps = len(self.steps)
            for i in range(len(priority)):
                time = priority[i][1]
                items_to_add = [time[1]]
                does_improve = self.does_improve(items_to_add, i)
                if not does_improve:
                    if time[1] == OBSIDIAN:
                        items_to_add = [CLAY, OBSIDIAN]
                        does_improve = self.does_improve(items_to_add, priority[i][0])
                        if not does_improve:
                            items_to_add = [ORE, CLAY, OBSIDIAN]
                            does_improve = self.does_improve(items_to_add, priority[i][0])
                    elif time[1] == CLAY:
                        items_to_add = [ORE, CLAY]
                        does_improve = self.does_improve(items_to_add, priority[i][0])
                if does_improve:
                    self.add_steps(items_to_add, priority[i][0])
                    priority = self._calc_optimization_priority()
                    break

    def does_improve(self, robots: List[str], index: int) -> bool:
        current_total_time = self._get_total_time(self.steps)
        new_steps = self.steps[:index] + [WaitAndBuild(robot, self.blueprint.robot_cost[robot]) for robot in robots] + self.steps[index:]
        new_total_time = self._get_total_time(new_steps)
        return new_total_time < current_total_time and new_total_time < 24

    def get_wait_times(self, steps: List[WaitAndBuild]) -> List[Tuple[int, str]]:
        inventory = Materials({})
        robots = {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
        wait_times = []
        for step in steps:
            wait_time, resource = step.get_wait_time(inventory, robots)
            inventory.mul_add(robots, wait_time + 1)
            inventory.decrease(self.blueprint.robot_cost[step.robot])
            robots[step.robot] += 1
            wait_times.append((wait_time, resource))
        return wait_times

    def get_total_time(self) -> int:
        return self._get_total_time(self.steps)

    def _get_total_time(self, steps: List[WaitAndBuild]) -> int:
        wait_times = self.get_wait_times(steps)
        return sum(map(lambda t: t[0], wait_times)) + len(wait_times)

    def get_num_geodes(self) -> int:
        inventory = Materials({})
        robots = {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
        total_time = 0
        for step in self.steps:
            wait_time, resource = step.get_wait_time(inventory, robots)
            if total_time + wait_time + 1 <= 24:
                inventory.mul_add(robots, wait_time + 1)
                inventory.decrease(self.blueprint.robot_cost[step.robot])
                robots[step.robot] += 1
                total_time += wait_time + 1
            else:
                remaining_time = 24 - total_time
                inventory.mul_add(robots, remaining_time)
                total_time += remaining_time
                break
        return inventory.items[GEODE]


def parse_input_file() -> List[Blueprint]:
    lines = read_input_file(19)
    return list(map(Blueprint, lines))


def calc_best_num_geodes(blueprint: Blueprint) -> int:
    strategy = Strategy(blueprint)
    return strategy.get_num_geodes()


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
