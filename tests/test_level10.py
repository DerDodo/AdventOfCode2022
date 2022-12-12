from level10 import level10_1, level10_2


def test_level10_1():
    assert level10_1() == 13140
    result = level10_2()
    assert result.count("#") == 124
