from typing import Tuple

from util.file_util import read_input_file


SNAFU_TO_DECIMAL = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}


BASE_5_TO_SNAFU = {
    0: ("0", 0),
    1: ("1", 0),
    2: ("2", 0),
    3: ("=", 1),
    4: ("-", 1),
    5: ("0", 1),
}


def snafu_to_decimal(snafu: str) -> int:
    result = 0
    for digit in snafu:
        result = result * 5 + SNAFU_TO_DECIMAL[digit]
    return result


def decimal_to_snafu(decimal: int) -> str:
    base_5 = decimal_to_base_5(decimal)
    result = ""
    while base_5 > 0:
        num = base_5 % 10
        snafu_digit = BASE_5_TO_SNAFU[num]
        result = snafu_digit[0] + result
        base_5 = (base_5 // 10) + snafu_digit[1]
    return result


def decimal_to_base_5(decimal: int) -> int:
    result = 0
    digit = 0
    while decimal > 0:
        result = result + (decimal % 5) * 10**digit
        digit += 1
        decimal = decimal // 5
    return result


def level25() -> Tuple[str, int]:
    fuel_requirements = read_input_file(25)
    sum_fuel_requirements = sum(map(snafu_to_decimal, fuel_requirements))
    return decimal_to_snafu(sum_fuel_requirements), 0


if __name__ == "__main__":
    _snafu, _num = level25()
    print(f"SNAFU: {_snafu}")
