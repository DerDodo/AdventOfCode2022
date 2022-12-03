from collections import Counter
from typing import List, Set
from numpy import array_split


class Rucksack:
    content: str
    compartment1: str
    compartment2: str

    def __init__(self, content: str):
        content = content.strip()
        compartment_length = int(len(content) / 2)
        self.content = content
        self.compartment1 = content[0:compartment_length]
        self.compartment2 = content[compartment_length:]

    def find_wrong_item(self) -> str:
        for item in self.compartment1:
            if item in self.compartment2:
                return item
        raise Exception("Couldn't find a wrong item")


def parse_input_file1(input_file_name: str) -> List[Rucksack]:
    file = open(input_file_name, "r")
    lines = file.readlines()
    all_rucksacks: List[Rucksack] = list()
    for line in lines:
        line = line.strip()
        all_rucksacks.append(Rucksack(line))
    return all_rucksacks


def parse_input_file2(input_file_name: str) -> List[List[Rucksack]]:
    file = open(input_file_name, "r")
    lines = file.readlines()
    all_rucksacks: List[Rucksack] = list(map(Rucksack, lines))
    rucksack_groups: List[List[Rucksack]] = array_split(all_rucksacks, len(all_rucksacks) / 3)
    return rucksack_groups


def get_item_priority(item: str) -> int:
    i = ord(item)
    if i >= 97:  # lower case letters
        return i - 96
    else:
        return i - (65 - 27)


def rucksack2set(rucksack: Rucksack) -> Set[str]:
    content = set()
    for character in rucksack.content:
        content.add(character)
    return content


def find_badge(rucksacks: List[Rucksack]) -> str:
    contents = list(map(lambda rucksack: Counter(rucksack2set(rucksack)), rucksacks))
    overlap = list((contents[0] & contents[1] & contents[2]).elements())
    if len(overlap) != 1:
        print("Couldn't reduce rucksacks:(" + str(len(overlap)) + ") " + ",".join(overlap))
    return overlap[0]


if __name__ == '__main__':
    rucksacks1 = parse_input_file1("input-files/level3-1.txt")
    wrong_items = map(Rucksack.find_wrong_item, rucksacks1)
    wrong_item_priorities = map(get_item_priority, wrong_items)
    print("Wrong item priority: " + str(sum(wrong_item_priorities)))

    rucksacks2 = parse_input_file2("input-files/level3-1.txt")
    badges = map(find_badge, rucksacks2)
    badges_priorities = map(get_item_priority, badges)
    print("Badge priority: " + str(sum(badges_priorities)))


