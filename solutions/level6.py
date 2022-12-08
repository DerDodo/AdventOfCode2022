from typing import List, Tuple

from util.file_util import read_input_file


def is_all_distinct(characters: List[int]) -> bool:
    char_set = set()
    for c in characters:
        if c in char_set:
            return False
        else:
            char_set.add(c)
    return True


def find_signal_start(text: str, num_characters: int) -> int:
    c = []
    for i in range(num_characters):
        c.append(text[i])
    i = num_characters - 1
    while i < len(text):
        c[num_characters - 1] = text[i]
        if is_all_distinct(c):
            return i + 1
        for j in range(num_characters - 1):
            c[j] = c[j + 1]
        i += 1
    raise ValueError("Couldn't find start signal!")


def level6() -> Tuple[int, int]:
    signal_buffer = read_input_file(6)[0]
    signal_start4 = find_signal_start(signal_buffer, 4)
    signal_start14 = find_signal_start(signal_buffer, 14)
    return signal_start4, signal_start14


if __name__ == '__main__':
    _signal_start4, _signal_start14 = level6()
    print(f"Signal start 4: {_signal_start4}")
    print(f"Signal start 14: {_signal_start14}")
