from level12 import level12


def test_level12():
    _num_steps1, _num_steps2 = level12()
    assert _num_steps1 == 31
    assert _num_steps2 == 29
