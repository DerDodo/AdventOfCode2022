from level22 import level22, WrapType


def test_level22():
    assert level22(WrapType.Map) == 6032
    assert level22(WrapType.Cube, 0) == 5031
