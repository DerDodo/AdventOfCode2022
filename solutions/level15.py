import time
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

    def calc_signal_spots_for_line(self, y: int) -> List[Position]:
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

        return line

    def get_uncovered_x(self, y: int, limit_x: int) -> int | None:
        signal_ranges: List[Tuple[int, int]] = list()

        for sensor in self.sensors:
            distance_sensor_to_beacon = sensor.get_distance()
            distance_sensor_to_y = abs(sensor.position_y - y)
            signal_for_y = distance_sensor_to_beacon - distance_sensor_to_y
            if signal_for_y >= 0:
                signal_ranges.append((sensor.position_x - signal_for_y, sensor.position_x + signal_for_y))

        signal_ranges.sort(key=lambda r: r[0] * 10000000 + r[1])

        check_x = 0
        for signal_range in signal_ranges:
            if check_x >= signal_range[0]:
                check_x = max(check_x, signal_range[1] + 1)
            else:
                return check_x

        if check_x < limit_x:
            return check_x
        else:
            return None


def parse_input_file() -> Field:
    lines = read_input_file(15)
    return Field(lines)


def level15(y_level_1: int, max_level_2: int) -> Tuple[int, int]:
    field = parse_input_file()

    level_1_line = field.calc_signal_spots_for_line(y_level_1)
    level_1 = len(list(filter(lambda p: p == Position.Signal, level_1_line)))

    for y in range(0, max_level_2 + 1):
        if y > 0 and y % 10000 == 0:  # prevent for tests
            print(f"Checking line {y}", flush=True)
        uncovered_x = field.get_uncovered_x(y, max_level_2)
        if uncovered_x is not None:
            return level_1, uncovered_x * 4000000 + y


if __name__ == "__main__":
    startTime = time.time()
    _signal_spots, _tuning_frequency = level15(2000000, 4000000)
    print(f"Signal spots: {_signal_spots}")
    print(f"Tuning frequency: {_tuning_frequency}")
    executionTime = time.time() - startTime
    print("Execution time in seconds: " + str(executionTime))
