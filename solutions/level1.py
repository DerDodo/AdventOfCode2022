from typing import List, Tuple

from util.file_util import read_input_file


class Elf:
    items: List[int]

    def __init__(self):
        self.items = list()

    def add(self, item: int):
        self.items.append(item)

    def total_weight(self):
        return sum(self.items)


def parse_input_file() -> List[Elf]:
    lines = read_input_file(1)
    all_elves: List[Elf] = list()
    new_elf = Elf()
    for line in lines:
        if line == "":
            all_elves.append(new_elf)
            new_elf = Elf()
        else:
            new_elf.add(int(line))
    all_elves.append(new_elf)
    return all_elves


def level1() -> Tuple[Elf, int]:
    elves = parse_input_file()
    elves.sort(key=Elf.total_weight, reverse=True)

    max_elf = elves[0]
    max_three_elves_weight = sum(map(Elf.total_weight, elves[0:3]))
    return max_elf, max_three_elves_weight


if __name__ == '__main__':
    _max_elf, _max_three_elves_weight = level1()
    print("Max carrying elf: " + str(_max_elf.total_weight()))
    print("Max 3 carrying elves: " + str(_max_three_elves_weight))
