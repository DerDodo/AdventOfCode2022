from collections import Counter
from typing import List, Set, Tuple
from numpy import array_split

from util.file_util import read_input_file


class Rucksack:
    content: str
    compartment1: str
    compartment2: str

    def __init__(self, content: str):
        compartment_length = int(len(content) / 2)
        self.content = content
        self.compartment1 = content[0:compartment_length]
        self.compartment2 = content[compartment_length:]

    def find_wrong_item(self) -> str:
        for item in self.compartment1:
            if item in self.compartment2:
                return item
        raise ValueError("Couldn't find a wrong item")


def parse_input_file1() -> List[Rucksack]:
    lines = read_input_file(3)
    all_rucksacks = list(map(Rucksack, lines))
    return all_rucksacks


def parse_input_file2() -> List[List[Rucksack]]:
    lines = read_input_file(3)
    all_rucksacks = list(map(Rucksack, lines))
    rucksack_groups = array_split(all_rucksacks, len(all_rucksacks) / 3)
    return rucksack_groups


def get_item_priority(item: str) -> int:
    i = ord(item)
    if i >= 97:  # lower case letters
        return i - 96
    else:  # upper case letters
        return i - (65 - 27)


def rucksack2set(rucksack: Rucksack) -> Set[str]:
    content = set()
    for character in rucksack.content:
        content.add(character)
    return content


def find_badge(rucksacks: List[Rucksack]) -> str:
    contents = list(map(lambda rucksack: Counter(rucksack2set(rucksack)), rucksacks))
    overlap = list((contents[0] & contents[1] & contents[2]).elements())
    return overlap[0]


def level3() -> Tuple[int, int]:
    rucksacks1 = parse_input_file1()
    wrong_items = map(Rucksack.find_wrong_item, rucksacks1)
    wrong_item_priorities = map(get_item_priority, wrong_items)

    rucksacks2 = parse_input_file2()
    badges = map(find_badge, rucksacks2)
    badges_priorities = map(get_item_priority, badges)

    return sum(wrong_item_priorities), sum(badges_priorities)


if __name__ == '__main__':
    wrong_item_priority, badges_priority = level3()
    print(f"Wrong item priority: {wrong_item_priority}")
    print(f"Badge priority: {badges_priority}")
