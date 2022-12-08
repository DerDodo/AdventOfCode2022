from solutions.level6 import level6, find_signal_start


def test_level6():
    _signal_start4, _signal_start14 = level6()
    assert _signal_start4 == 7
    assert _signal_start14 == 19

    assert find_signal_start("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert find_signal_start("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert find_signal_start("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
    assert find_signal_start("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11

    assert find_signal_start("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert find_signal_start("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert find_signal_start("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert find_signal_start("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26
