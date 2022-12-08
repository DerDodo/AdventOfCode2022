from solutions.level1 import level1


def test_level1():
    _max_elf, _max_three_elves_weight = level1()
    assert _max_elf.total_weight() == 24000
    assert _max_three_elves_weight == 45000
