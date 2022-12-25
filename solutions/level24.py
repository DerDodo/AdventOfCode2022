from enum import Enum
from typing import List, Tuple, Set

from util.file_util import read_input_file


class Movement(Enum):
    Up = "^"
    Down = "v"
    Left = "<"
    Right = ">"
    Wait = "x"

    def get_movement(self) -> Tuple[int, int]:
        if self == Movement.Up:
            return 0, -1
        elif self == Movement.Down:
            return 0, 1
        elif self == Movement.Left:
            return -1, 0
        elif self == Movement.Right:
            return 1, 0
        elif self == Movement.Wait:
            return 0, 0


BlizzardData = Tuple[int, int, Movement]
FieldDimensions = Tuple[int, int]
Coordinate = Tuple[int, int]


class Field:
    start: Tuple[int, int]
    end: Tuple[int, int]
    blizzards: List[Set[Tuple[int, int]]]
    walls: Set[Tuple[int, int]]
    width: int
    height: int

    def __init__(self, lines: List[str]):
        self.start = 1, 0
        self.end = len(lines[0]) - 2, len(lines) - 1
        self.blizzards = []
        self.walls = set()
        self.width = len(lines[0])
        self.height = len(lines)

        directions = [m.value for m in Movement]
        blizzards = []
        for y in range(self.height):
            for x in range(self.width):
                if lines[y][x] == "#":
                    self.walls.add((x, y))
                elif lines[y][x] in directions:
                    blizzards.append((x, y, Movement(lines[y][x])))

        for minute in range(1000):
            self.blizzards.append(set())

        for blizzard in blizzards:
            x = blizzard[0] - 1
            y = blizzard[1] - 1
            for minute in range(1000):
                self.blizzards[minute].add((x + 1, y + 1))
                movement = blizzard[2].get_movement()
                x = (x + movement[0]) % (self.width - 2)
                y = (y + movement[1]) % (self.height - 2)

    def get_possible_movements(self, x: int, y: int, minute: int):
        movements = []
        for movement in Movement:
            x_plus, y_plus = movement.get_movement()
            check_x = x + x_plus
            check_y = y + y_plus
            position = (check_x, check_y)
            if 0 <= check_y < self.height and position not in self.blizzards[minute] and position not in self.walls:
                movements.append(movement)
        return movements

    def get_distance_to_end(self, x: int, y: int):
        return abs(x - self.end[0]) + abs(y - self.end[1])


def parse_input_file() -> Field:
    lines = read_input_file(24)
    return Field(lines)


def level24_trip(field: Field, start: Tuple[int, int, int], end: Tuple[int, int]) -> int:
    todo = [start]
    todo_set = {start}
    i = 0
    while i < 10000000 and len(todo) != 0:
        position = todo.pop(0)
        if position[0] == end[0] and position[1] == end[1]:
            return position[2]
        possible_movements = field.get_possible_movements(position[0], position[1], position[2] + 1)
        for movement in possible_movements:
            delta = movement.get_movement()
            todo_entry = (position[0] + delta[0], position[1] + delta[1], position[2] + 1)
            if todo_entry not in todo_set:
                todo.append(todo_entry)
                todo_set.add(todo_entry)
        i += 1
    raise ValueError("Couldn't find exit!")


def level24() -> Tuple[int, int]:
    field = parse_input_file()
    minutes_trip_1 = level24_trip(field, (field.start[0], field.start[1], 0), field.end)
    minutes_trip_2 = level24_trip(field, (field.end[0], field.end[1], minutes_trip_1), field.start)
    minutes_trip_3 = level24_trip(field, (field.start[0], field.start[1], minutes_trip_2), field.end)
    return minutes_trip_1, minutes_trip_3


if __name__ == "__main__":
    _minutes_to_exit, _minutes_to_round_trip = level24()
    print(f"Minutes to exit: {_minutes_to_exit}")
    print(f"Minutes to round trip: {_minutes_to_round_trip}")
