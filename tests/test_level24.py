from level24 import level24


def test_level24():
    _minutes_to_exit, _minutes_to_round_trip = level24()
    assert _minutes_to_exit == 18
    assert _minutes_to_round_trip == 54
