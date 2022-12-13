from functools import cmp_to_key
from typing import List, Any

from util.file_util import read_input_file


class Packet:
    description: str
    value: List[Any]

    def __init__(self, description: str):
        self.description = description
        self.value = eval(description)


class PacketPair:
    id: int
    left: Packet
    right: Packet

    def __init__(self, _id: int, left: Packet, right: Packet):
        self.id = _id
        self.left = left
        self.right = right

    def is_in_right_order(self) -> bool:
        return compare_list(self.left.value, self.right.value)


def compare_ints(left: int, right: int) -> bool | None:
    if left < right:
        return True
    elif left > right:
        return False
    else:
        return


def compare_items(left: Any, right: Any) -> bool | None:
    left_is_list = isinstance(left, list)
    left_is_int = isinstance(left, int)
    right_is_list = isinstance(right, list)
    right_is_int = isinstance(right, int)

    if left_is_int and right_is_int:
        is_in_order = compare_ints(left, right)
        if is_in_order is not None:
            return is_in_order
    else:
        new_left = left if left_is_list else [left]
        new_right = right if right_is_list else [right]
        is_in_order = compare_list(new_left, new_right)
        if is_in_order is not None:
            return is_in_order


def compare_list(left_list: List[Any], right_list: List[Any]) -> bool | None:
    for i in range(len(left_list)):
        if i >= len(right_list):
            return False

        is_in_order = compare_items(left_list[i], right_list[i])
        if is_in_order is not None:
            return is_in_order

    if len(left_list) == len(right_list):
        return
    else:
        return True


def compare_packets(left: Packet, right: Packet) -> int:
    in_right_order = compare_list(left.value, right.value)
    if in_right_order:
        return -1
    elif not in_right_order:
        return 1
    else:
        return 0


def parse_input_file_in_pairs() -> List[PacketPair]:
    lines = read_input_file(13)
    packet_pairs: List[PacketPair] = []
    for i in range(0, len(lines), 3):
        packet_pairs.append(PacketPair(int(i / 3) + 1, Packet(lines[i]), Packet(lines[i + 1])))
    return packet_pairs


def parse_input_file_as_list() -> List[Packet]:
    lines = read_input_file(13)
    packets: List[Packet] = []
    for line in lines:
        if line != "":
            packets.append(Packet(line))
    packets.append(Packet("[[2]]"))
    packets.append(Packet("[[6]]"))
    return packets


def level13_1() -> int:
    packet_pairs = parse_input_file_in_pairs()
    packets_in_right_order = filter(PacketPair.is_in_right_order, packet_pairs)
    sum_ids = sum(map(lambda p: p.id, packets_in_right_order))
    return sum_ids


def level13_2() -> int:
    packets = parse_input_file_as_list()
    packets.sort(key=cmp_to_key(compare_packets))
    result = 1
    for i in range(len(packets)):
        if packets[i].description == "[[2]]" or packets[i].description == "[[6]]":
            result *= i + 1
    return result


if __name__ == '__main__':
    _result_value1 = level13_1()
    _result_value2 = level13_2()
    print(f"Result value (1): {_result_value1}")
    print(f"Result value (2): {_result_value2}")
