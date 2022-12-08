from solutions.level5 import level5


def test_level5():
    _top_items1, _top_items2 = level5()
    assert _top_items1 == "CMZ"
    assert _top_items2 == "MCD"
