from level15 import level15


def test_level15():
    _signal_spots, _num = level15(10)
    assert _signal_spots == 26
