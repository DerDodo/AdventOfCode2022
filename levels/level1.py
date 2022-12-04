from typing import List

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
    lines = read_input_file(1, 1)
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


if __name__ == '__main__':
    elves = parse_input_file()
    elves.sort(key=Elf.total_weight, reverse=True)

    max_elf = elves[0]
    print("Max carrying elf: " + str(max_elf.total_weight()))

    max_three_elves_weight = sum(map(Elf.total_weight, elves[0:3]))
    print("Max 3 carrying elves: " + str(max_three_elves_weight))
