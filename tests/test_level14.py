from level14 import level14


def test_level14():
    _num_sand_units1, _num_sand_units2 = level14()
    assert _num_sand_units1 == 24
    assert _num_sand_units2 == 93
