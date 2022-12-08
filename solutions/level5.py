from typing import List, Tuple

from util.file_util import read_input_file


class Command:
    move_from: int
    move_to: int
    amount: int

    def __init__(self, line: str):
        parts = line.split(" ")
        self.amount = int(parts[1])
        self.move_from = int(parts[3]) - 1
        self.move_to = int(parts[5]) - 1


class Cargo:
    stacks: List[List[str]]

    def __init__(self, crates: List[List[str]]):
        self.stacks = crates


def revert_stacks(in_stacks: List[List[str]]) -> List[List[str]]:
    stacks: List[List[str]] = [[] for _ in range(len(in_stacks))]
    for j in range(len(in_stacks)):
        for _ in range(len(in_stacks[j])):
            stacks[j].append(in_stacks[j].pop())
    return stacks


def parse_input_file() -> Tuple[Cargo, List[Command]]:
    lines = read_input_file(5, False)
    num_crates = int((len(lines[0]) + 1) / 4)
    all_commands: List[Command] = []
    # read first in order, then reverse pop to true location
    temp_stacks: List[List[str]] = [[] for _ in range(num_crates)]
    read_stacks = True

    for line in lines:
        if line == "\n":
            read_stacks = False
        elif read_stacks:
            for j in range(num_crates):
                char = line[j * 4 + 1]
                if char != " " and not char.isdecimal():
                    temp_stacks[j].append(char)
        else:
            all_commands.append(Command(line))

    stacks = revert_stacks(temp_stacks)

    return Cargo(stacks), all_commands


def get_top(_stack: List[str]) -> str:
    return _stack[-1]


def level5() -> Tuple[str, str]:
    cargo1, commands = parse_input_file()
    for command in commands:
        for _ in range(command.amount):
            character = cargo1.stacks[command.move_from].pop()
            cargo1.stacks[command.move_to].append(character)

    cargo2, commands = parse_input_file()
    for command in commands:
        temp_stack: List[str] = []
        for _ in range(command.amount):
            character = cargo2.stacks[command.move_from].pop()
            temp_stack.append(character)
        for _ in range(command.amount):
            cargo2.stacks[command.move_to].append(temp_stack.pop())

    top_items_1 = ''.join(list(map(get_top, cargo1.stacks)))
    top_items_2 = ''.join(list(map(get_top, cargo2.stacks)))
    return top_items_1, top_items_2


if __name__ == '__main__':
    _top_items1, _top_items2 = level5()
    print(f"Top items 1: {_top_items1}")
    print(f"Top items 2: {_top_items2}")
