from typing import Tuple, List

from level25 import level25, snafu_to_decimal, decimal_to_snafu, decimal_to_base_5

TEST_DATA: List[Tuple] = [
    # snafu, dec, base-5
    ("1=-0-2", 1747, 23442),
    ("12111", 906, 12111),
    ("2=0=", 198, 1243),
    ("21", 11, 21),
    ("2=01", 201, 1301),
    ("111", 31, 111),
    ("20012", 1257, 20012),
    ("112", 32, 112),
    ("1=-1=", 353, 2403),
    ("1-12", 107, 412),
    ("12", 7, 12),
    ("1=", 3, 3),
    ("122", 37, 122),
]


def test_level25():
    _snafu, _num = level25()
    assert _snafu == "2=-1=0"


def test_snafu_to_dec():
    for test_data in TEST_DATA:
        assert snafu_to_decimal(test_data[0]) == test_data[1]


def test_dec_to_snafu():
    for test_data in TEST_DATA:
        assert decimal_to_snafu(test_data[1]) == test_data[0]


def test_dec_to_base_5():
    for test_data in TEST_DATA:
        assert decimal_to_base_5(test_data[1]) == test_data[2]
