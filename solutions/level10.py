from typing import Dict

from util.file_util import read_input_file


def parse_input_file() -> Dict[int, int]:
    lines = read_input_file(10)
    value_at_cycle: Dict[int, int] = {}
    cycle = 1
    value = 1
    for line in lines:
        value_at_cycle[cycle] = value
        if line == "noop":
            cycle += 1
        else:
            parts = line.split(" ")
            if parts[0] == "addx":
                add_value = int(parts[1])
                cycle += 1
                value_at_cycle[cycle] = value
                cycle += 1
                value += add_value
            else:
                raise ValueError(f"Couldn't parse line: {line}")
    return value_at_cycle


def level10_1() -> int:
    value_at_cycle = parse_input_file()
    result = 0
    for target_cycle in [20, 60, 100, 140, 180, 220]:
        result += target_cycle * value_at_cycle[target_cycle]
    return result


def level10_2() -> str:
    value_at_cycle = parse_input_file()
    output = ""
    for i in range(240):
        value = value_at_cycle[i + 1]
        distance = abs(value - i % 40)
        if distance < 2:
            output += "#"
        else:
            output += "."
    return output


if __name__ == '__main__':
    print(f"Signal strength: {level10_1()}")
    _result = level10_2()
    for _i in range(0, 240, 40):
        print(_result[_i:_i+40])
