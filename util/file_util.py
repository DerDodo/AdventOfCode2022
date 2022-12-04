from typing import List


def read_input_file(level_id: int, file_id: int) -> List[str]:
    input_file = open(f"input-files/level{level_id}-{file_id}.txt", "r")
    lines = input_file.readlines()
    lines = [line.strip() for line in lines]
    return lines
