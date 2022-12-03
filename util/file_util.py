from typing import List


def read_input_file(level: int, file: int) -> List[str]:
    file = open(f"input-files/level{level}-{file}.txt", "r")
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines
