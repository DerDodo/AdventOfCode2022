from enum import Enum
from typing import List, Set, Tuple

from util.file_util import read_input_file


class GridEntry(Enum):
    Lava = 0
    Water = 1
    InnerAir = 2


class Droplet:
    lava_set: Set[int]
    grid: List[List[List[GridEntry]]]
    grid_size_x: int
    grid_size_y: int
    grid_size_z: int

    def __init__(self, lines: List[str]):
        self.grid_size_x, self.grid_size_y, self.grid_size_z = 0, 0, 0
        for line in lines:
            coordinates = list(map(lambda coord: int(coord), line.split(",")))
            # Make the grid bigger to make sure every cell is filled by the floodfill
            self.grid_size_x = max(self.grid_size_x, coordinates[0] + 2)
            self.grid_size_y = max(self.grid_size_y, coordinates[1] + 2)
            self.grid_size_z = max(self.grid_size_z, coordinates[2] + 2)

        self.lava_set = set()
        self.grid = [
            [[GridEntry.InnerAir for _ in range(self.grid_size_z)] for _ in range(self.grid_size_y)]
            for _ in range(self.grid_size_x)
        ]
        for line in lines:
            coordinates = list(map(lambda coord: int(coord), line.split(",")))
            self.lava_set.add(self.get_grid_id(coordinates[0], coordinates[1], coordinates[2]))
            self.grid[coordinates[0]][coordinates[1]][coordinates[2]] = GridEntry.Lava

        self.fill_outer_surface()

    def fill_outer_surface(self):
        check_fields_set: Set[int] = set()
        check_fields: List[Tuple[int, int, int]] = [(self.grid_size_x - 1, 0, 0)]
        check_fields_set.add(self.get_grid_id(self.grid_size_x - 1, 0, 0))
        self.grid[self.grid_size_x - 1][0][0] = GridEntry.Water

        i = 0
        while i < len(check_fields):
            x, y, z = check_fields[i]
            if self.grid[x][y][z] == GridEntry.Lava:
                continue

            for plus in [-1, 1]:
                if self.should_check_for_outer_air(x + plus, y, z, check_fields_set):
                    self.grid[x + plus][y][z] = GridEntry.Water
                    check_fields.append((x + plus, y, z))
                    check_fields_set.add(self.get_grid_id(x + plus, y, z))

                if self.should_check_for_outer_air(x, y + plus, z, check_fields_set):
                    self.grid[x][y + plus][z] = GridEntry.Water
                    check_fields.append((x, y + plus, z))
                    check_fields_set.add(self.get_grid_id(x, y + plus, z))

                if self.should_check_for_outer_air(x, y, z + plus, check_fields_set):
                    self.grid[x][y][z + plus] = GridEntry.Water
                    check_fields.append((x, y, z + plus))
                    check_fields_set.add(self.get_grid_id(x, y, z + plus))
            i += 1

    def should_check_for_outer_air(self, x: int, y: int, z: int, check_fields_set: Set[int]) -> bool:
        return (
            0 <= x < self.grid_size_x
            and 0 <= y < self.grid_size_y
            and 0 <= z < self.grid_size_z
            and self.grid[x][y][z] != GridEntry.Lava
            and self.get_grid_id(x, y, z) not in check_fields_set
        )

    def get_grid_id(self, x: int, y: int, z: int) -> int:
        return z * self.grid_size_y * self.grid_size_x + y * self.grid_size_x + x

    def get_grid_coordinates(self, _id: int) -> Tuple[int, int, int]:
        z = _id // (self.grid_size_y * self.grid_size_x)
        y = (_id % (self.grid_size_y * self.grid_size_x)) // self.grid_size_x
        x = _id % self.grid_size_x
        return x, y, z

    def calc_surface_area(self) -> int:
        surface_area = 0
        for grid_id in self.lava_set:
            x, y, z = self.get_grid_coordinates(grid_id)
            surface_area += self.is_surface(x + 1, y, z)
            surface_area += self.is_surface(x - 1, y, z)
            surface_area += self.is_surface(x, y + 1, z)
            surface_area += self.is_surface(x, y - 1, z)
            surface_area += self.is_surface(x, y, z + 1)
            surface_area += self.is_surface(x, y, z - 1)
        return surface_area

    def is_surface(self, x, y, z) -> int:
        if 0 <= x < self.grid_size_x and 0 <= y < self.grid_size_y and 0 <= z < self.grid_size_z:
            return 1 if self.grid[x][y][z] != GridEntry.Lava else 0
        else:
            return 1

    def calc_outer_surface_area(self):
        surface_area = 0
        for grid_id in self.lava_set:
            x, y, z = self.get_grid_coordinates(grid_id)
            surface_area += self.is_outer_surface(x + 1, y, z)
            surface_area += self.is_outer_surface(x - 1, y, z)
            surface_area += self.is_outer_surface(x, y + 1, z)
            surface_area += self.is_outer_surface(x, y - 1, z)
            surface_area += self.is_outer_surface(x, y, z + 1)
            surface_area += self.is_outer_surface(x, y, z - 1)
        return surface_area

    def is_outer_surface(self, x, y, z) -> int:
        if 0 <= x < self.grid_size_x and 0 <= y < self.grid_size_y and 0 <= z < self.grid_size_z:
            return 1 if self.grid[x][y][z] == GridEntry.Water else 0
        else:
            return 1


def level18(lines: List[str]) -> Tuple[int, int]:
    droplet = Droplet(lines)
    return droplet.calc_surface_area(), droplet.calc_outer_surface_area()


if __name__ == "__main__":
    _surface_area, _outer_surface_area = level18(read_input_file(18))
    print(f"Surface area: {_surface_area}")
    print(f"Outer surface area: {_outer_surface_area}")
