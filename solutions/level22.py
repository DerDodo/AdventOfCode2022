from enum import Enum
from typing import List, Tuple

from util.file_util import read_input_file


class WrapType(Enum):
    Map = 0,
    Cube = 1


class Tile(Enum):
    Void = " ",
    Free = ".",
    Wall = "#",


class Direction(Enum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3

    def get_char(self) -> str:
        if self == Direction.Right:
            return ">"
        elif self == Direction.Up:
            return "^"
        elif self == Direction.Left:
            return "<"
        else:
            return "v"

    def rotate_left(self):
        if self == Direction.Right:
            return Direction.Up
        elif self == Direction.Up:
            return Direction.Left
        elif self == Direction.Left:
            return Direction.Down
        else:
            return Direction.Right

    def rotate_right(self):
        if self == Direction.Right:
            return Direction.Down
        elif self == Direction.Down:
            return Direction.Left
        elif self == Direction.Left:
            return Direction.Up
        else:
            return Direction.Right

    def get_steps(self) -> Tuple[int, int]:
        if self == Direction.Right:
            return 1, 0
        elif self == Direction.Left:
            return -1, 0
        elif self == Direction.Up:
            return 0, -1
        else:
            return 0, 1


class Map:
    wrap_type: WrapType
    cube_layout: int
    tiles: List[List[Tile]]
    path: List[str]
    used_path: List[List[str]]

    def __init__(self, wrap_type: WrapType, lines: List[str], cube_layout: int = -1):
        self.wrap_type = wrap_type
        self.cube_layout = cube_layout
        tiles_reverse = {
            " ": Tile.Void,
            ".": Tile.Free,
            "#": Tile.Wall,
        }

        self.tiles = list(map(lambda line: [tiles_reverse[c] for c in line[:-1]], lines[:-2]))
        self.used_path = list(map(lambda tiles: ["." for _ in tiles], self.tiles))
        self.path = []
        path = lines[-1]
        number = ""
        for char in path:
            if char == "R" or char == "L":
                self.path.append(number)
                number = ""
                self.path.append(char)
            else:
                number += char
        self.path.append(number)

    def get_password(self) -> int:
        x, y = self._find_start_x(), 0
        direction = Direction.Right
        for part in self.path:
            if part == "L":
                direction = direction.rotate_left()
            elif part == "R":
                direction = direction.rotate_right()
            else:
                x, y, direction = self._walk(x, y, direction, int(part))
        return self._calc_password(x, y, direction)

    def _walk(self, x: int, y: int, direction: Direction, steps: int) -> Tuple[int, int, Direction]:
        for _ in range(steps):
            x, y, direction, stop = self._walk_step(x, y, direction)
            if stop:
                break
        return x, y, direction

    def _walk_step(self, x: int, y: int, direction: Direction) -> Tuple[int, int, Direction, bool]:
        step_x, step_y = direction.get_steps()
        new_x = x + step_x
        new_y = y + step_y
        tile_type = self._get_type(new_x, new_y)
        self.used_path[y][x] = direction.get_char()
        if tile_type == Tile.Wall:
            return x, y, direction, True
        elif tile_type == Tile.Free:
            return new_x, new_y, direction, False
        elif tile_type == Tile.Void:
            new_x, new_y, new_direction, wrap_tile_type = self._wrap_around(x, y, direction)
            if wrap_tile_type == Tile.Free:
                return new_x, new_y, new_direction, False
            elif wrap_tile_type == Tile.Wall:
                return x, y, direction, True
            else:
                raise ValueError(f"Wrap around returned Void, x: {x}, y: {y}, new_x: {new_x}, new_y: {new_y}, direction: {direction}")
        else:
            raise ValueError(f"Unknown type type {tile_type} at x: {new_x}, y: {new_y}")

    def _wrap_around(self, x: int, y: int, direction: Direction) -> Tuple[int, int, Direction, Tile]:
        if self.wrap_type == WrapType.Map:
            return self._wrap_around_map(x, y, direction)
        else:
            if self.cube_layout == 0:
                return self._wrap_around_cube_layout_0(x, y, direction)
            elif self.cube_layout == 1:
                return self._wrap_around_cube_layout_1(x, y, direction)
            else:
                raise ValueError(f"Unknown cube layout {self.cube_layout}")

    def _wrap_around_map(self, x: int, y: int, direction: Direction) -> Tuple[int, int, Direction, Tile]:
        step_x, step_y = direction.get_steps()
        tile_type = Tile.Free
        while tile_type != Tile.Void:
            x -= step_x
            y -= step_y
            tile_type = self._get_type(x, y)
        return x + step_x, y + step_y, direction, self._get_type(x + step_x, y + step_y)

    def _wrap_around_cube_layout_0(self, x: int, y: int, direction: Direction) -> Tuple[int, int, Direction, Tile]:
        face = self._get_face_id(x, y)
        face_length = self._get_face_length()
        face_x = x % face_length
        face_y = y % face_length
        if face == 1 and direction == Direction.Up:  # 1 -> 2
            target_x = face_length - (face_x + 1)
            target_y = face_length
            target_direction = Direction.Down
        elif face == 1 and direction == Direction.Right:  # 1 -> 6
            target_x = face_x * 4 - 1
            target_y = face_length * 3 - (face_y + 1)
            target_direction = Direction.Left
        elif face == 1 and direction == Direction.Left:  # 1 -> 3
            target_x = face_length * 2 - (face_y + 1)
            target_y = face_length
            target_direction = Direction.Down
        elif face == 2 and direction == Direction.Up:  # 2 -> 1
            target_x = face_length * 3 - (face_x + 1)
            target_y = 0
            target_direction = Direction.Down
        elif face == 2 and direction == Direction.Left:  # 2 -> 6
            target_x = face_length * 4 - (face_y + 1)
            target_y = face_length * 3 - 1
            target_direction = Direction.Up
        elif face == 2 and direction == Direction.Down:  # 2 -> 5
            target_x = face_length * 3 - (face_x + 1)
            target_y = face_length * 3 - 1
            target_direction = Direction.Up
        elif face == 3 and direction == Direction.Up:  # 3 -> 1
            target_x = face_length * 2
            target_y = face_x
            target_direction = Direction.Right
        elif face == 3 and direction == Direction.Down:  # 3 -> 5
            target_x = face_length * 2
            target_y = face_length * 2 + face_x
            target_direction = Direction.Right
        elif face == 4 and direction == Direction.Right:  # 4 -> 6
            target_x = face_length * 4 - (face_y + 1)
            target_y = face_length * 2
            target_direction = Direction.Down
        elif face == 5 and direction == Direction.Left:  # 5 -> 3
            target_x = face_length * 2 - (face_y + 1)
            target_y = face_length * 2 - 1
            target_direction = Direction.Up
        elif face == 5 and direction == Direction.Down:  # 5 -> 2
            target_x = face_length - (face_x + 1)
            target_y = face_length * 2 - 1
            target_direction = Direction.Up
        elif face == 6 and direction == Direction.Up:  # 6 -> 4
            target_x = face_length * 3 - 1
            target_y = face_length * 2 - (face_x + 1)
            target_direction = Direction.Left
        elif face == 6 and direction == Direction.Right:  # 6 -> 1
            target_x = face_length * 3 - 1
            target_y = face_length - (face_y + 1)
            target_direction = Direction.Left
        elif face == 6 and direction == Direction.Down:  # 6 -> 2
            target_x = 0
            target_y = face_length * 2 - (face_x + 1)
            target_direction = Direction.Right
        else:
            raise ValueError(f"Cannot walk around corner: face: {face}, x: {x}, y: {y}, direction: {direction}")

        return target_x, target_y, target_direction, self._get_type(target_x, target_y)

    def _wrap_around_cube_layout_1(self, x: int, y: int, direction: Direction) -> Tuple[int, int, Direction, Tile]:
        face = self._get_face_id(x, y)
        face_length = self._get_face_length()
        face_x = x % face_length
        face_y = y % face_length
        if face == 1 and direction == Direction.Up:  # 1 -> 6
            target_x = 0
            target_y = face_length * 3 + face_x
            target_direction = Direction.Right
            assert self._get_face_id(target_x, target_y) == 6
        elif face == 1 and direction == Direction.Left:  # 1 -> 4
            target_x = 0
            target_y = face_length * 3 - (face_y + 1)
            target_direction = Direction.Right
            assert self._get_face_id(target_x, target_y) == 4
        elif face == 2 and direction == Direction.Up:  # 2 -> 6
            target_x = face_x
            target_y = face_length * 4 - 1
            target_direction = Direction.Up
            assert self._get_face_id(target_x, target_y) == 6
        elif face == 2 and direction == Direction.Right:  # 2 -> 5
            target_x = face_length * 2 - 1
            target_y = face_length * 3 - (face_y + 1)
            target_direction = Direction.Left
            assert self._get_face_id(target_x, target_y) == 5
        elif face == 2 and direction == Direction.Down:  # 2 -> 3
            target_x = face_length * 2 - 1
            target_y = face_length + face_x
            target_direction = Direction.Left
            assert self._get_face_id(target_x, target_y) == 3
        elif face == 3 and direction == Direction.Left:  # 3 -> 4
            target_x = face_y
            target_y = face_length * 2
            target_direction = Direction.Down
            assert self._get_face_id(target_x, target_y) == 4
        elif face == 3 and direction == Direction.Right:  # 3 -> 2
            target_x = face_length * 2 + face_y
            target_y = face_length - 1
            target_direction = Direction.Up
            assert self._get_face_id(target_x, target_y) == 2
        elif face == 4 and direction == Direction.Up:  # 4 -> 3
            target_x = face_length
            target_y = face_length + face_x
            target_direction = Direction.Right
            assert self._get_face_id(target_x, target_y) == 3
        elif face == 4 and direction == Direction.Left:  # 4 -> 1
            target_x = face_length
            target_y = face_length - (face_y + 1)
            target_direction = Direction.Right
            assert self._get_face_id(target_x, target_y) == 1
        elif face == 5 and direction == Direction.Right:  # 5 -> 2
            target_x = face_length * 3 - 1
            target_y = face_length - (face_y + 1)
            target_direction = Direction.Left
            assert self._get_face_id(target_x, target_y) == 2
        elif face == 5 and direction == Direction.Down:  # 5 -> 6
            target_x = face_length - 1
            target_y = face_length * 3 + face_x
            target_direction = Direction.Left
            assert self._get_face_id(target_x, target_y) == 6
        elif face == 6 and direction == Direction.Left:  # 6 -> 1
            target_x = face_length + face_x
            target_y = 0
            target_direction = Direction.Down
            assert self._get_face_id(target_x, target_y) == 1
        elif face == 6 and direction == Direction.Down:  # 6 -> 2
            target_x = face_length * 2 + face_x
            target_y = 0
            target_direction = Direction.Down
            assert self._get_face_id(target_x, target_y) == 2
        elif face == 6 and direction == Direction.Right:  # 6 -> 5
            target_x = face_length + face_y
            target_y = face_length * 3 - 1
            target_direction = Direction.Up
            assert self._get_face_id(target_x, target_y) == 5
        else:
            raise ValueError(f"Cannot walk around corner: face: {face}, x: {x}, y: {y}, direction: {direction}")

        return target_x, target_y, target_direction, self._get_type(target_x, target_y)

    def _get_face_id(self, x: int, y: int) -> int:
        face_size = self._get_face_length()
        face_x = x // face_size
        face_y = y // face_size
        if self.cube_layout == 0:
            return self._get_face_id_layout_0(face_x, face_y)
        elif self.cube_layout == 1:
            return self._get_face_id_layout_1(face_x, face_y)
        else:
            raise ValueError(f"Unknown cube layout {self.cube_layout}")

    def _get_face_id_layout_0(self, face_x: int, face_y: int) -> int:
        if face_y == 0 and face_x == 2: return 1
        elif face_y == 1 and face_x == 0: return 2
        elif face_y == 1 and face_x == 1: return 3
        elif face_y == 1 and face_x == 2: return 4
        elif face_y == 2 and face_x == 2: return 5
        elif face_y == 2 and face_x == 3: return 6
        raise ValueError(f"Cannot find face! face_x: {face_x},  face_y: {face_y}")

    def _get_face_id_layout_1(self, face_x: int, face_y: int) -> int:
        if face_y == 0 and face_x == 1: return 1
        elif face_y == 0 and face_x == 2: return 2
        elif face_y == 1 and face_x == 1: return 3
        elif face_y == 2 and face_x == 0: return 4
        elif face_y == 2 and face_x == 1: return 5
        elif face_y == 3 and face_x == 0: return 6
        raise ValueError(f"Cannot find face! face_x: {face_x},  face_y: {face_y}")

    def _get_face_length(self) -> int:
        if self.cube_layout == 0:
            return len(self.tiles) // 3
        elif self.cube_layout == 1:
            return len(self.tiles) // 4
        else:
            raise ValueError(f"Unknown cube layout {self.cube_layout}")

    def _get_type(self, x: int, y: int) -> Tile:
        if y < 0 or y >= len(self.tiles):
            return Tile.Void

        tiles = self.tiles[y]
        if x < 0 or x >= len(tiles):
            return Tile.Void

        return tiles[x]

    @staticmethod
    def _calc_password(x: int, y: int, direction: Direction) -> int:
        return 1000 * (y + 1) + (x + 1) * 4 + direction.value

    def _find_start_x(self) -> int:
        return self.tiles[0].index(Tile.Free)

    def print_path(self):
        for y in range(len(self.tiles)):
            tiles = self.tiles[y]
            line = ""
            for x in range(len(tiles)):
                tile = tiles[x]
                if tile == Tile.Free:
                    line += self.used_path[y][x]
                elif tile == Tile.Void:
                    line += " "
                else:
                    line += "#"
            print(line)


def parse_input_file(wrap_type: WrapType, cube_layout: int) -> Map:
    lines = read_input_file(22, False)
    return Map(wrap_type, lines, cube_layout)


def level22(wrap_type: WrapType, cube_layout: int = -1) -> int:
    field = parse_input_file(wrap_type, cube_layout)
    password = field.get_password()
    field.print_path()
    return password


if __name__ == "__main__":
    #print(f"Password (map): {level22(WrapType.Map)}")
    print(f"Password (cube): {level22(WrapType.Cube, 1)}")
