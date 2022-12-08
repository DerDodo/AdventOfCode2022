from abc import abstractmethod
from typing import List, Dict, Tuple

from util.file_util import read_input_file


class Item:
    @abstractmethod
    def get_size(self) -> int:
        pass


class File(Item):
    size: int
    name: str

    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size


class Directory(Item):
    name: str
    items: Dict[str, Item]

    def __init__(self, parent, name: str):
        self.parent = parent
        self.name = name
        self.items = {}

    def get_size(self) -> int:
        return sum(map(lambda item: item.get_size(), self.items.values()))

    def get_parent(self):
        return self.parent

    def create_directory(self, name: str):
        if name not in self.items:
            self.items[name] = Directory(self, name)

    def get_subdirectory(self, name: str):
        if name not in self.items:
            self.create_directory(name)
        item = self.items[name]
        if isinstance(item, Directory):
            return item
        else:
            raise TypeError(f"Item {name} is not a directory.")

    def create_file(self, name: str, size: int):
        if name not in self.items:
            new_file = File(name, size)
            self.items[name] = new_file


def change_dir(root: Directory, current_dir: Directory, command: List[str]) -> Directory:
    if command[1] == "/":
        return root
    elif command[1] == "..":
        return current_dir.parent
    else:
        return current_dir.get_subdirectory(command[1])


def read_contents(current_dir: Directory, lines: List[str], i: int) -> int:
    while i + 1 != len(lines) and not lines[i + 1].startswith("$"):
        i += 1
        entry = lines[i].split(" ")
        if entry[0] == "dir":
            current_dir.create_directory(entry[1])
        else:
            current_dir.create_file(entry[1], int(entry[0]))
    return i


def parse_input() -> Directory:
    lines = read_input_file(7)
    root = Directory(None, "/")
    current_dir: Directory | None = None

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("$"):
            command = line[2:].split(" ")
            if command[0] == "cd":
                current_dir = change_dir(root, current_dir, command)
            elif command[0] == "ls":
                i = read_contents(current_dir, lines, i)
            else:
                raise ValueError(f"Unknown command {command}, line {i + 1}")
        i += 1

    return root


def get_all_directories(root: Directory) -> List[Directory]:
    all_directories = [root]
    for key in root.items:
        item = root.items[key]
        if isinstance(item, Directory):
            all_directories.extend(get_all_directories(item))
    return all_directories


def level7() -> Tuple[int, int]:
    file_structure = parse_input()
    directories = get_all_directories(file_structure)

    small_directories = list(filter(lambda item: item.get_size() <= 100000, directories))
    level_1_size = sum(map(Directory.get_size, small_directories))

    max_space = 70000000
    needed_space = 30000000
    usable_space = max_space - needed_space
    used_space = file_structure.get_size()
    space_to_delete = used_space - usable_space
    big_directories = list(filter(lambda item: item.get_size() > space_to_delete, directories))
    level_2_size = min(map(Directory.get_size, big_directories))

    return level_1_size, level_2_size


if __name__ == '__main__':
    _level_1_size, _level_2_size = level7()
    print(f"Level 1 size: {_level_1_size}")
    print(f"Level 2 size: {_level_2_size}")
