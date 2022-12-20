from typing import List

from util.file_util import read_input_file


class Number:
    value: int
    id: int

    def __init__(self, value: str, _id: int, decryption_key: int):
        self.value = int(value) * decryption_key
        self.id = _id


def parse_input_file(decryption_key: int) -> List[Number]:
    lines = read_input_file(20)
    return list(map(lambda line: Number(line[1], line[0], decryption_key), enumerate(lines)))


def _print(numbers: List[Number]):
    print(", ".join(map(lambda n: str(n.value), numbers)))


def level20(num_shuffles: int, decryption_key: int) -> int:
    numbers = parse_input_file(decryption_key)
    shuffled = parse_input_file(decryption_key)
    n = len(numbers)

    for _ in range(num_shuffles):
        for number_i in range(len(numbers)):
            move_value = numbers[number_i]
            move_index = 0
            for index, x in enumerate(shuffled):
                if x.id == move_value.id:
                    move_index = index
                    break
            number = shuffled.pop(move_index)
            target = (move_index + number.value) % (n - 1)
            shuffled.insert(target, number)

    i0 = list(map(lambda v: v.value, shuffled)).index(0)
    return shuffled[(1000 + i0) % n].value + shuffled[(2000 + i0) % n].value + shuffled[(3000 + i0) % n].value


if __name__ == "__main__":
    _coordinate_sum_1 = level20(1, 1)
    print(f"Coordinate sum (1): {_coordinate_sum_1}")
    _coordinate_sum_10 = level20(10, 811589153)
    print(f"Coordinate sum (10): {_coordinate_sum_10}")
