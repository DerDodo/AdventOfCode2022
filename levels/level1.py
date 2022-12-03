from typing import List


class Elf:
    items: List[int]

    def __init__(self):
        self.items = list()

    def add(self, item: int):
        self.items.append(item)

    def total_weight(self):
        return sum(self.items)


def parse_input_file(input_file_name) -> List[Elf]:
    file = open(input_file_name, "r")
    lines = file.readlines()
    all_elves: List[Elf] = list()
    new_elf = Elf()
    for line in lines:
        line = line.strip()
        if line == "":
            all_elves.append(new_elf)
            new_elf = Elf()
        else:
            new_elf.add(int(line))
    all_elves.append(new_elf)
    return all_elves


if __name__ == '__main__':
    elves = parse_input_file("input-files/level1-1.txt")
    elves.sort(key=Elf.total_weight, reverse=True)

    max_elf = elves[0]
    print("Max carrying elf: " + str(max_elf.total_weight()))

    max_three_elves_weigth = elves[0].total_weight() + elves[1].total_weight() + elves[2].total_weight()
    print("Max 3 carrying elves: " + str(max_three_elves_weigth))

