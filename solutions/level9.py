from typing import List, Set, Tuple

from math_util import clamp
from util.file_util import read_input_file


class Knot:
    x: int
    y: int

    def __init__(self):
        self.x = self.y = 0


class Rope:
    knots: List[Knot]
    tail_positions: Set[str]

    def __init__(self, length: int):
        self.knots = [Knot() for _ in range(length)]
        self.tail_positions = set()
        self.store_tail_position()

    def get_head(self):
        return self.knots[0]

    def store_tail_position(self):
        tail = self.knots[-1]
        position_id = f"{tail.x}-{tail.y}"
        self.tail_positions.add(position_id)

    def move_rope(self):
        for i in range(1, len(self.knots), 1):
            self.move_knot(i)
        self.store_tail_position()

    def move_knot(self, knot_id):
        knot = self.knots[knot_id]
        predecessor = self.knots[knot_id - 1]

        distance_x = predecessor.x - knot.x
        distance_y = predecessor.y - knot.y
        if abs(distance_x) > 1 or abs(distance_y) > 1:
            knot.x += clamp(distance_x)
            knot.y += clamp(distance_y)


class Movement:
    direction: str
    steps: int

    def __init__(self, line: str):
        parts = line.split(" ")
        self.direction = parts[0]
        self.steps = int(parts[1])

    def execute(self, rope: Rope):
        for _ in range(self.steps):
            self.execute_step(rope)
            rope.move_rope()

    def execute_step(self, rope: Rope):
        if self.direction == "U":
            rope.get_head().y += 1
        elif self.direction == "D":
            rope.get_head().y -= 1
        elif self.direction == "R":
            rope.get_head().x += 1
        elif self.direction == "L":
            rope.get_head().x -= 1
        else:
            raise ValueError(f"Unknown direction {self.direction}")


def parse_input() -> List[Movement]:
    lines = read_input_file(9)
    return list(map(Movement, lines))


def level9(movements: List[Movement]) -> Tuple[int, int]:
    rope_2 = Rope(2)
    for movement in movements:
        movement.execute(rope_2)

    rope_10 = Rope(10)
    for movement in movements:
        movement.execute(rope_10)

    return len(rope_2.tail_positions), len(rope_10.tail_positions)


if __name__ == '__main__':
    _movements = parse_input()
    _num_places_visited_2, _num_places_visited_10 = level9(_movements)
    print(f"Num places visited (2): {_num_places_visited_2}")
    print(f"Num places visited (10): {_num_places_visited_10}")
