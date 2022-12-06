from typing import List

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
            print(''.join(c))
            return i + 1
        for j in range(num_characters - 1):
            c[j] = c[j + 1]
        i += 1
    raise ValueError("Couldn't find start signal!")


if __name__ == '__main__':
    buffer = read_input_file(6, 1)[0]
    signal_start = find_signal_start(buffer, 14)

    print(f"Signal start: {signal_start}")
