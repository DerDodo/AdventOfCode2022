from level19 import level19


def test_level19():
    _sum_quality_1, _geode_product_2 = level19()
    assert _sum_quality_1 == 33
    assert _geode_product_2 == 62 * 56
