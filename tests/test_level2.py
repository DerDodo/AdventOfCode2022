from solutions.level2 import level2


def test_level2():
    score_round_1, score_round_2 = level2()
    assert score_round_1 == 15
    assert score_round_2 == 12
