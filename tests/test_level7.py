from solutions.level7 import level7


def test_level7():
    _level_1_size, _level_2_size = level7()
    assert _level_1_size == 95437
    assert _level_2_size == 24933642
