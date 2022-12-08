from solutions.level4 import level4


def test_level3():
    _num_full_overlaps, _num_partly_overlaps = level4()
    assert _num_full_overlaps == 2
    assert _num_partly_overlaps == 4
