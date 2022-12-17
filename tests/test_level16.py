from level16_1 import level16_1
from level16_2 import level16_2


def test_level16_1():
    _max_pressure = level16_1([])
    assert _max_pressure == 1651


def test_level16_2():
    _max_pressure = level16_2(["JJ", "BB"], ["DD", "HH"])
    assert _max_pressure == 1707
