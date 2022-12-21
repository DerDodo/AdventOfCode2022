from collections import defaultdict
from typing import List, Dict, Tuple

from util.file_util import read_input_file


FinishedMonkeys = Dict[str, int]


class UnfinishedMonkey:
    left: str
    right: str
    operation: str
    num_finished_parts: int

    def __init__(self, shout: str):
        parts = shout.split(" ")
        self.left = parts[0]
        self.operation = parts[1]
        self.right = parts[2]
        self.num_finished_parts = 0

    def eval(self, finished_monkeys: FinishedMonkeys) -> int:
        if self.operation == "+":
            return finished_monkeys[self.left] + finished_monkeys[self.right]
        elif self.operation == "-":
            return finished_monkeys[self.left] - finished_monkeys[self.right]
        elif self.operation == "*":
            return finished_monkeys[self.left] * finished_monkeys[self.right]
        elif self.operation == "/":
            return finished_monkeys[self.left] // finished_monkeys[self.right]
        else:
            raise ValueError(f"Operation {self.operation} unknown")


UnfinishedMonkeys = Dict[str, UnfinishedMonkey]
UnfinishedMonkeyLookup = Dict[str, List[UnfinishedMonkey]]


def parse_input_file() -> Tuple[FinishedMonkeys, UnfinishedMonkeys]:
    lines = read_input_file(21)
    finished_monkeys = {}
    unfinished_monkeys = {}
    for line in lines:
        monkey_name = line[0:4]
        monkey_shout = line[6:]
        if monkey_shout.isdecimal():
            finished_monkeys[monkey_name] = int(monkey_shout)
        else:
            unfinished_monkeys[monkey_name] = UnfinishedMonkey(monkey_shout)
    return finished_monkeys, unfinished_monkeys


def finish_monkey(finished_monkey: str, unfinished_monkey_lookup: UnfinishedMonkeyLookup):
    for unfinished_monkey in unfinished_monkey_lookup[finished_monkey]:
        unfinished_monkey.num_finished_parts += 1


def level21_1() -> int:
    finished_monkeys, unfinished_monkeys = parse_input_file()
    unfinished_monkey_lookup: UnfinishedMonkeyLookup = defaultdict(list)
    for unfinished_monkey in unfinished_monkeys.values():
        unfinished_monkey_lookup[unfinished_monkey.left].append(unfinished_monkey)
        unfinished_monkey_lookup[unfinished_monkey.right].append(unfinished_monkey)

    for finished_monkey in finished_monkeys:
        finish_monkey(finished_monkey, unfinished_monkey_lookup)

    monkeys_to_finish = list(filter(lambda m: unfinished_monkeys[m].num_finished_parts == 2, unfinished_monkeys))
    while len(monkeys_to_finish) > 0:
        for monkey_to_finish in monkeys_to_finish:
            monkey = unfinished_monkeys[monkey_to_finish]
            value = monkey.eval(finished_monkeys)
            finished_monkeys[monkey_to_finish] = value
            finish_monkey(monkey_to_finish, unfinished_monkey_lookup)
            unfinished_monkeys.pop(monkey_to_finish)
        monkeys_to_finish = list(filter(lambda m: unfinished_monkeys[m].num_finished_parts == 2, unfinished_monkeys))

    return finished_monkeys["root"]


if __name__ == "__main__":
    _number = level21_1()
    print(f"Monkey number: {_number}")
