from typing import List

from solutions.level9 import level9, Movement, parse_input
from util.file_util import read_input_file_id


def parse_input2() -> List[Movement]:
    lines = read_input_file_id(9, 2)
    return list(map(Movement, lines))


def test_level9_1():
    _movements = parse_input()
    _num_places_visited_2, _num_places_visited_10 = level9(_movements)
    assert _num_places_visited_2 == 13
    assert _num_places_visited_10 == 1


def test_level9_2():
    _movements = parse_input2()
    _num_places_visited_2, _num_places_visited_10 = level9(_movements)
    assert _num_places_visited_2 == 88
    assert _num_places_visited_10 == 36
