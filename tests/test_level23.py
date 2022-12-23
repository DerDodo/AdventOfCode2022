from level23 import level23


def test_level23():
    _covered_area, _final_round = level23()
    assert _covered_area == 110
    assert _final_round == 20
