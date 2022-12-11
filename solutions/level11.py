from functools import reduce
from math import floor
from operator import mul
from typing import Dict, List, Any

from util.file_util import read_input_file


class Monkey:
    id: int
    items: List[int]
    operation: str
    test_target: int
    targets: Dict[bool, int]
    inspection_count: int

    def __init__(self, _id: int):
        self.id = _id
        self.items = []
        self.operation = ""
        self.test_target = 1
        self.targets = {}
        self.inspection_count = 0

    def throw_all_items(self, monkeys: Dict[int, Any], worry_decrease: int, max_worry: int):
        for item in self.items:
            new = eval(self.operation, {'old': item})
            new = floor(new / worry_decrease)
            new = new % max_worry
            target = new % self.test_target == 0
            target_monkey_id = self.targets[target]
            monkeys[target_monkey_id].items.append(new)
            self.inspection_count += 1
        self.items.clear()


def read_monkey(lines: List[str]) -> Monkey:
    if not lines[0].startswith("Monkey "):
        raise ValueError(f"Line is no monkey: {lines[0]}")

    id_str = lines[0][-2]
    items_str = lines[1][len("Starting items: "):]
    operation_str = lines[2][len("Operation: new = "):]
    test_str = lines[3][len("Test: divisible by "):]
    true_str = lines[4][-1]
    false_str = lines[5][-1]

    monkey = Monkey(int(id_str))
    items = list(map(lambda _i: eval(_i), items_str.split(",")))
    monkey.items = items
    monkey.operation = operation_str
    monkey.test_target = int(test_str)
    monkey.targets[True] = int(true_str)
    monkey.targets[False] = int(false_str)

    return monkey


def parse_input_file() -> Dict[int, Monkey]:
    lines = read_input_file(11)
    monkey_dict: Dict[int, Monkey] = {}
    for i in range(0, len(lines), 7):
        new_monkey = read_monkey(lines[i:i+6])
        monkey_dict[new_monkey.id] = new_monkey
    return monkey_dict


def level11(worry_decrease: int, rounds: int) -> int:
    monkeys = parse_input_file()
    max_worry = reduce(mul, map(lambda m: m.test_target, monkeys.values()), 1)
    for _ in range(rounds):
        for monkey in monkeys.values():
            monkey.throw_all_items(monkeys, worry_decrease, max_worry)
    inspection_counts = list(map(lambda m: m.inspection_count, monkeys.values()))
    inspection_counts.sort(reverse=True)
    return inspection_counts[0] * inspection_counts[1]


if __name__ == '__main__':
    print(f"Monkey business (1): {level11(3, 20)}")
    print(f"Monkey business (2): {level11(1, 10000)}")
