from level17 import level17


def test_level17_0():
    assert level17(0) == 0


def test_level17_1():
    assert level17(1) == 1


def test_level17_2():
    assert level17(2) == 4


def test_level17_3():
    assert level17(3) == 6


def test_level17_4():
    assert level17(4) == 7


def test_level17_5():
    assert level17(5) == 9


def test_level17_6():
    assert level17(6) == 10


def test_level17_7():
    assert level17(7) == 13


def test_level17_8():
    assert level17(8) == 15


def test_level17_9():
    assert level17(9) == 17


def test_level17_10():
    assert level17(10) == 17


def test_level17_2022():
    assert level17(2022, print_height_differences=False) == 3068


def test_level17_2022_with_pattern():
    assert level17(2022, 15, 50 - 15) == 3068


def test_level17_1000000000000():
    assert level17(1000000000000, 15, 50 - 15) == 1514285714288
