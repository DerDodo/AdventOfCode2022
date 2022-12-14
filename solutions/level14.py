from enum import Enum
from typing import List, Tuple

from util.file_util import read_input_file


class Material(Enum):
    AIR = "."
    STONE = "#"
    SAND = "o"


class Line:
    start_x: int
    start_y: int
    end_x: int
    end_y: int

    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def get_coordinates(self) -> List[Tuple[int, int]]:
        current_x = min(self.end_x, self.start_x)
        current_y = min(self.end_y, self.start_y)
        distance_x = abs(self.end_x - self.start_x)
        distance_y = abs(self.end_y - self.start_y)
        max_distance = max(distance_x, distance_y)
        step_x = 1 if distance_x > distance_y else 0
        step_y = 1 if distance_y > distance_x else 0

        coordinates = []
        for _ in range(max_distance + 1):
            coordinates.append((current_x, current_y))
            current_x += step_x
            current_y += step_y
        return coordinates


class Structure:
    area: List[List[Material]]
    sand_start_x: int
    height: int

    def __init__(self, lines: List[Line], add_floor: bool):
        min_x, max_x, max_y = 1000000, 0, 0
        for line in lines:
            min_x = min(min_x, line.start_x, line.end_x)
            max_x = max(max_x, line.start_x, line.end_x)
            max_y = max(max_y, line.start_y, line.end_y)
        distance_x = max_x - min_x + 1
        distance_y = max_y + 1

        if add_floor:
            distance_y += 2
            max_y += 2
            min_x -= distance_y
            max_x += distance_y
            distance_x += 2 * distance_y
            lines.append(Line(min_x, max_y, max_x, max_y))

        self.sand_start_x = 500 - min_x
        self.height = max_y
        area = [[Material.AIR] * distance_x for _ in range(distance_y)]
        for line in lines:
            for coordinate in line.get_coordinates():
                y = coordinate[1]
                x = coordinate[0] - min_x
                area[y][x] = Material.STONE
        self.area = area

    def fill(self):
        spot_x, spot_y = self.find_next_sand_spot()
        while spot_x is not None:
            self.area[spot_y][spot_x] = Material.SAND
            spot_x, spot_y = self.find_next_sand_spot()
            if spot_x == self.sand_start_x and spot_y == 0:
                self.area[spot_y][spot_x] = Material.SAND
                return

    def find_next_sand_spot(self, ) -> Tuple[int | None, int | None]:
        last_check_x, last_check_y = -1, -1
        check_x, check_y = self.sand_start_x, 0
        while last_check_x != check_x and last_check_y != check_y:
            last_check_x, last_check_y = check_x, check_y
            if check_y == self.height:
                return None, None
            while self.area[check_y + 1][check_x] == Material.AIR:
                check_y += 1
                if check_y == self.height:
                    return None, None
            if self.area[check_y + 1][check_x - 1] == Material.AIR:
                check_x -= 1
                check_y += 1
            elif self.area[check_y + 1][check_x + 1] == Material.AIR:
                check_x += 1
                check_y += 1
        return check_x, check_y

    def get_num_sand(self) -> int:
        return sum(map(lambda area_line: len(list(filter(lambda point: point == Material.SAND, area_line))), self.area))

    def print(self):
        for line in self.area:
            print("".join(map(lambda c: c.value, line)))

    def print_to_file(self):
        out_file = open("structure.txt", "w")
        for line in self.area:
            line = "".join(map(lambda c: c.value, line)) + "\n"
            out_file.write(line)
        out_file.close()


def parse_input_file() -> List[Line]:
    file_lines = read_input_file(14)
    lines: List[Line] = []
    for file_line in file_lines:
        str_coordinates = file_line.split(" -> ")
        coordinates: List[Tuple[int, int]] = []
        for str_coordinate in str_coordinates:
            parts = str_coordinate.split(",")
            coordinates.append((int(parts[0]), int(parts[1])))
        start = coordinates[0]
        for i in range(1, len(coordinates), 1):
            end = coordinates[i]
            lines.append(Line(start[0], start[1], end[0], end[1]))
            start = end
    return lines


def level14() -> Tuple[int, int]:
    structure1 = Structure(parse_input_file(), False)
    structure1.fill()
    structure2 = Structure(parse_input_file(), True)
    structure2.fill()
    return structure1.get_num_sand(), structure2.get_num_sand()


if __name__ == '__main__':
    _num_sand_units1, _num_sand_units2 = level14()
    print(f"Num sand units (1): {_num_sand_units1}")
    print(f"Num sand units (2): {_num_sand_units2}")
