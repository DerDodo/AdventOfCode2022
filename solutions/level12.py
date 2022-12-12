from typing import List, Tuple

from util.file_util import read_input_file


class Landscape:
    height: List[List[int]]  # y,x
    steps_to_end: List[List[int]]  # y,x
    start: Tuple[int, int]  # y,x
    end: Tuple[int, int]  # y,x

    def __init__(self, lines: List[str]):
        self.height = []
        for y in range(len(lines)):
            new_line = []
            for x in range(len(lines[y])):
                c = lines[y][x]
                if c == "S":
                    new_line.append(0)
                    self.start = y, x
                elif c == "E":
                    new_line.append(25)
                    self.end = y, x
                else:
                    new_line.append(ord(c) - ord("a"))
            self.height.append(new_line)
        self.start_flood_fill()

    def get_path_length(self):
        return self.steps_to_end[self.start[0]][self.start[1]]

    def start_flood_fill(self):
        self.steps_to_end = list(map(lambda line: list(map(lambda _: 10000000, line)), self.height))
        self.steps_to_end[self.end[0]][self.end[1]] = 0
        self.flood_fill(self.end[1], self.end[0])

    def flood_fill(self, x: int, y: int):
        filled_fields = self.set_neighbors(x, y)
        for field in filled_fields:
            self.flood_fill(field[1], field[0])

    def set_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        filled_fields: List[Tuple] = []
        source_height = self.height[y][x]
        source_steps = self.steps_to_end[y][x]
        for y_plus, x_plus in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            check_y = y + y_plus
            check_x = x + x_plus
            if 0 <= check_y < len(self.steps_to_end) and 0 <= check_x < len(self.steps_to_end[check_y]):
                target_height = self.height[check_y][check_x]
                if target_height - source_height > -2 and self.steps_to_end[check_y][check_x] > source_steps + 1:
                    self.steps_to_end[check_y][check_x] = source_steps + 1
                    filled_field = (check_y, check_x)
                    filled_fields.append(filled_field)
        return filled_fields


def parse_input_file() -> Landscape:
    lines = read_input_file(12)
    return Landscape(lines)


def get_minimal_path_from_a(landscape: Landscape) -> int:
    min_steps = 1000000
    for y in range(len(landscape.steps_to_end)):
        for x in range(len(landscape.steps_to_end[y])):
            if landscape.height[y][x] == 0:
                min_steps = min(min_steps, landscape.steps_to_end[y][x])
    return min_steps


def level12() -> Tuple[int, int]:
    landscape = parse_input_file()
    num_steps1 = landscape.get_path_length()
    num_steps2 = get_minimal_path_from_a(landscape)
    return num_steps1, num_steps2


if __name__ == '__main__':
    _num_steps1, _num_steps2 = level12()
    print(f"Num steps (1): {_num_steps1}")
    print(f"Num steps (2): {_num_steps2}")
