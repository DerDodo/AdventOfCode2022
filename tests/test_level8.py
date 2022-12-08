from solutions.level8_1 import level8_1
from solutions.level8_2 import level8_2


def test_level8_1():
    _num_visible_trees = level8_1()
    assert _num_visible_trees == 21


def test_level8_2():
    _num_visible_trees = level8_2()
    assert _num_visible_trees == 8
