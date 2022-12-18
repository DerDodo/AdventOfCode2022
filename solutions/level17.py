from typing import List, Set, Tuple

from util.file_util import read_input_file


def rock_str_to_array(rock: str) -> List[List[bool]]:
    lines = rock.split("\n")
    return list(map(lambda line: list(map(lambda char: char == "#", line)), lines))


def calc_field_id(x: int, y: int) -> int:
    return y * 7 + x


class Rock:
    fields: List[Tuple[int, int]]
    height: int
    width: int

    def __init__(self, definition):
        lines = rock_str_to_array(definition)
        self.fields = []
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                if lines[y][x]:
                    self.fields.append((x, y))
        self.height = len(lines)
        self.width = len(lines[0])


class Field:
    winds: List[int]
    rocks: List[Rock]
    filled_positions: Set[int]
    num_rocks_fallen = 0
    height = 0
    next_wind = 0

    def __init__(self, winds: str):
        self.winds = list(map(lambda wind: 1 if wind == ">" else -1, winds))
        self.rocks = [
            Rock("####"),
            Rock(".#.\n###\n.#."),
            Rock("..#\n..#\n###"),
            Rock("#\n#\n#\n#"),
            Rock("##\n##"),
        ]
        self.filled_positions = set()
        self.height = 0
        self.next_wind = 0

    def let_rocks_fall(self, num_rocks: int, print_height_differences: bool) -> int:
        last_all_rocks_height = 0
        for i in range(self.num_rocks_fallen, num_rocks + self.num_rocks_fallen):
            rock_id = i % len(self.rocks)
            rock = self.rocks[rock_id]
            x, y = 2, self.height + 2 + rock.height
            for _ in range(10000):
                x_plus = self.winds[self.next_wind]
                self.next_wind = (self.next_wind + 1) % len(self.winds)

                new_x = max(0, min(7 - rock.width, x + x_plus))
                if not self.does_rock_collide(rock, new_x, y):
                    x = new_x

                new_y = y - 1
                if self.does_rock_collide(rock, x, new_y):
                    self.height = max(y + 1, self.height)
                    if rock_id == len(self.rocks) - 1 and print_height_differences:
                        print(f"Height: {self.height} (+{self.height - last_all_rocks_height})," +
                              f" num rocks: {i + 1}, wind id: {self.next_wind}")
                        last_all_rocks_height = self.height
                    self.place(rock, x, y)
                    break
                else:
                    y = new_y
        return self.height

    def does_rock_collide(self, rock: Rock, x: int, y: int):
        if y - rock.height < -1:
            return True

        for field in rock.fields:
            test_x, test_y = x + field[0], y - field[1]
            if self.is_field_filled(test_x, test_y):
                return True

        return False

    def is_field_filled(self, x: int, y: int):
        place_id = calc_field_id(x, y)
        return place_id in self.filled_positions

    def place(self, rock: Rock, x: int, y: int):
        for field in rock.fields:
            place_id = calc_field_id(x + field[0], y - field[1])
            if place_id in self.filled_positions:
                raise ValueError(f"Field x={x + field[0]}, y={y - field[1]} is already filled!")
            self.filled_positions.add(place_id)

    def print_field(self, height: int):
        for y in range(height - 1, -1, -1):
            line = "|"
            for x in range(7):
                line += "#" if self.is_field_filled(x, y) else "."
            line += "|"
            print(line)
        print("+-------+")


def parse_input_file() -> Field:
    lines = read_input_file(17)
    return Field(lines[0])


def level17(
    num_rocks: int, pattern_start: int = -1, pattern_length: int = -1, print_height_differences: bool = False
) -> int:
    field = parse_input_file()
    if pattern_start == -1:
        return field.let_rocks_fall(num_rocks, print_height_differences)
    else:
        # Move to start of pattern
        start_height = field.let_rocks_fall(pattern_start, False)
        # Measure height of one pattern
        pattern_height = field.let_rocks_fall(pattern_length, False) - start_height
        # Measure rest after all patterns are done
        num_rocks -= pattern_start + pattern_length
        num_full_patterns = num_rocks // pattern_length
        final_height = field.let_rocks_fall(num_rocks - num_full_patterns * pattern_length, False)
        # Extrapolate patterns
        return final_height + num_full_patterns * pattern_height


if __name__ == "__main__":
    print(f"Height (2022): {level17(2022, print_height_differences=False)}")
    print(f"Height (100000): {level17(10000, print_height_differences=True)}")
    print(f"Height (100000): {level17(10000, 1725, 3420 - 1725)}")
    print(f"Height (100000): {level17(1000000000000, 1725, 3420 - 1725)}")
