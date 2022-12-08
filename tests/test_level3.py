from solutions.level3 import level3


def test_level3():
    wrong_item_priority, badges_priority = level3()
    assert wrong_item_priority == 157
    assert badges_priority == 70
