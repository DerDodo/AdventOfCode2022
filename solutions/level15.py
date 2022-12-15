from enum import Enum
from typing import List, Tuple

from util.file_util import read_input_file


class Sensor:
    position_x: int
    position_y: int
    beacon_x: int
    beacon_y: int

    def __init__(self, definition: str):
        parts = definition.split(" ")
        self.position_x = int(parts[2][2:-1])
        self.position_y = int(parts[3][2:-1])
        self.beacon_x = int(parts[-2][2:-1])
        self.beacon_y = int(parts[-1][2:])

    def get_distance(self) -> int:
        return abs(self.position_x - self.beacon_x) + abs(self.position_y - self.beacon_y)


class Position(Enum):
    Beacon = "B"
    Sensor = "S"
    Signal = "#"
    Unknown = "."


class Field:
    sensors: List[Sensor]
    width: int
    min_x: int
    max_x: int

    def __init__(self, definitions: List[str]):
        self.sensors = list(map(Sensor, definitions))
        self.min_x = 1000000
        self.max_x = -1000000
        for sensor in self.sensors:
            distance_sensor_to_beacon = sensor.get_distance()
            self.min_x = min(
                self.min_x, sensor.position_x - distance_sensor_to_beacon, sensor.position_x, sensor.beacon_x
            )
            self.max_x = max(
                self.max_x, sensor.position_x + distance_sensor_to_beacon, sensor.position_x, sensor.beacon_x
            )
        self.width = self.max_x - self.min_x + 1

    def calc_signal_spots_for_line(self, y: int) -> int:
        line = [Position.Unknown] * self.width

        for sensor in self.sensors:
            distance_sensor_to_beacon = sensor.get_distance()
            distance_sensor_to_y = abs(sensor.position_y - y)
            signal_for_y = distance_sensor_to_beacon - distance_sensor_to_y
            if signal_for_y >= 0:
                for i in range(-signal_for_y, signal_for_y + 1):
                    x = sensor.position_x - self.min_x + i
                    if 0 <= x < self.width:
                        line[x] = Position.Signal

        for sensor in self.sensors:
            if sensor.position_y == y:
                x = sensor.position_x - self.min_x
                line[x] = Position.Sensor
            if sensor.beacon_y == y:
                x = sensor.beacon_x - self.min_x
                line[x] = Position.Beacon

        # print("".join(map(lambda p: p.value, line)))
        return len(list(filter(lambda p: p == Position.Signal, line)))


def parse_input_file() -> Field:
    lines = read_input_file(15)
    return Field(lines)


def level15(y: int) -> Tuple[int, int]:
    field = parse_input_file()
    return field.calc_signal_spots_for_line(y), 0


if __name__ == "__main__":
    _signal_spots, _num = level15(2000000)
    print(f"Signal spots (1): {_signal_spots}")
