from level15 import level15


def test_level15():
    _signal_spots, _distress_beacon_frequency = level15(10, 20)
    assert _signal_spots == 26
    assert _distress_beacon_frequency == 56000011
