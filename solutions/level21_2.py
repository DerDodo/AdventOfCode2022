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
        if self.num_finished_parts != 2:
            raise ValueError(
                f"Only {self.num_finished_parts} part/s are finished: {self.left} {self.operation} {self.right}"
            )
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

    def find_unknown(self, target_number: int, finished_monkeys: FinishedMonkeys) -> Tuple[int, str]:
        if self.num_finished_parts != 1:
            raise ValueError(
                f"Need one finished part, got {self.num_finished_parts}!: {self.left} {self.operation} {self.right}"
            )

        if self.operation == "+":
            return self._revert_plus(target_number, finished_monkeys)
        elif self.operation == "-":
            return self._revert_minus(target_number, finished_monkeys)
        elif self.operation == "*":
            return self._revert_multiply(target_number, finished_monkeys)
        elif self.operation == "/":
            return self._revert_divide(target_number, finished_monkeys)
        else:
            raise ValueError(f"Operation {self.operation} unknown")

    def _revert_plus(self, target_number: int, finished_monkeys: FinishedMonkeys) -> Tuple[int, str]:
        if self.left in finished_monkeys:
            return target_number - finished_monkeys[self.left], self.right
        else:
            return target_number - finished_monkeys[self.right], self.left

    def _revert_minus(self, target_number: int, finished_monkeys: FinishedMonkeys) -> Tuple[int, str]:
        if self.left in finished_monkeys:
            return finished_monkeys[self.left] - target_number, self.right
        else:
            return target_number + finished_monkeys[self.right], self.left

    def _revert_multiply(self, target_number: int, finished_monkeys: FinishedMonkeys) -> Tuple[int, str]:
        if self.left in finished_monkeys:
            return target_number // finished_monkeys[self.left], self.right
        else:
            return target_number // finished_monkeys[self.right], self.left

    def _revert_divide(self, target_number: int, finished_monkeys: FinishedMonkeys) -> Tuple[int, str]:
        if self.left in finished_monkeys:
            return finished_monkeys[self.left] // target_number, self.right
        else:
            return target_number * finished_monkeys[self.right], self.left


UnfinishedMonkeys = Dict[str, UnfinishedMonkey]
UnfinishedMonkeyLookup = Dict[str, List[UnfinishedMonkey]]


def parse_input_file() -> Tuple[FinishedMonkeys, UnfinishedMonkeys]:
    lines = read_input_file(21)
    finished_monkeys = {}
    unfinished_monkeys = {}
    for line in lines:
        monkey_name = line[0:4]
        if monkey_name != "humn":
            monkey_shout = line[6:]
            if monkey_shout.isdecimal():
                finished_monkeys[monkey_name] = int(monkey_shout)
            else:
                unfinished_monkeys[monkey_name] = UnfinishedMonkey(monkey_shout)
    return finished_monkeys, unfinished_monkeys


def finish_monkey(finished_monkey: str, unfinished_monkey_lookup: UnfinishedMonkeyLookup):
    for unfinished_monkey in unfinished_monkey_lookup[finished_monkey]:
        unfinished_monkey.num_finished_parts += 1


def finish_monkeys(
    finished_monkeys: FinishedMonkeys,
    unfinished_monkeys: UnfinishedMonkeys,
    unfinished_monkey_lookup: UnfinishedMonkeyLookup,
):
    monkeys_to_finish = list(filter(lambda m: unfinished_monkeys[m].num_finished_parts == 2, unfinished_monkeys))
    while len(monkeys_to_finish) > 0:
        for monkey_to_finish in monkeys_to_finish:
            if monkey_to_finish == "root":
                return

            monkey = unfinished_monkeys[monkey_to_finish]
            value = monkey.eval(finished_monkeys)
            finished_monkeys[monkey_to_finish] = value
            finish_monkey(monkey_to_finish, unfinished_monkey_lookup)
            unfinished_monkeys.pop(monkey_to_finish)
        monkeys_to_finish = list(filter(lambda m: unfinished_monkeys[m].num_finished_parts == 2, unfinished_monkeys))


def setup() -> Tuple[FinishedMonkeys, UnfinishedMonkeys, UnfinishedMonkeyLookup]:
    finished_monkeys, unfinished_monkeys = parse_input_file()
    unfinished_monkey_lookup: UnfinishedMonkeyLookup = defaultdict(list)
    for unfinished_monkey in unfinished_monkeys.values():
        unfinished_monkey_lookup[unfinished_monkey.left].append(unfinished_monkey)
        unfinished_monkey_lookup[unfinished_monkey.right].append(unfinished_monkey)

    for finished_monkey in finished_monkeys:
        finish_monkey(finished_monkey, unfinished_monkey_lookup)

    finish_monkeys(finished_monkeys, unfinished_monkeys, unfinished_monkey_lookup)

    return finished_monkeys, unfinished_monkeys, unfinished_monkey_lookup


def find_target(
    finished_monkeys: FinishedMonkeys,
    unfinished_monkeys: UnfinishedMonkeys,
    unfinished_monkey_lookup: UnfinishedMonkeyLookup,
) -> Tuple[int, str]:
    finish_monkeys(finished_monkeys, unfinished_monkeys, unfinished_monkey_lookup)
    root = unfinished_monkeys["root"]
    if root.left in finished_monkeys:
        return finished_monkeys[root.left], root.right
    elif root.right in finished_monkeys:
        return finished_monkeys[root.right], root.left
    else:
        raise ValueError("Couldn't determine target")


def reverse_search(
    target_number: int,
    target_monkey_name: str,
    finished_monkeys: FinishedMonkeys,
    unfinished_monkeys: UnfinishedMonkeys,
) -> int:
    while target_monkey_name != "humn":
        monkey = unfinished_monkeys[target_monkey_name]
        target_number, target_monkey_name = monkey.find_unknown(target_number, finished_monkeys)
    return target_number


def level21_2() -> int:
    finished_monkeys, unfinished_monkeys, unfinished_monkey_lookup = setup()
    target_number, target_monkey_name = find_target(finished_monkeys, unfinished_monkeys, unfinished_monkey_lookup)
    return reverse_search(target_number, target_monkey_name, finished_monkeys, unfinished_monkeys)


if __name__ == "__main__":
    _number = level21_2()
    print(f"Monkey number: {_number}")
