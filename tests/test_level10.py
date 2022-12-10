from level10 import level10_1, level10_2


def test_level10_1():
    assert level10_1() == 13140
    result = level10_2()
    print("")
    for i in range(0, 240, 40):
        print(result[i:i+40])
    assert result.count("#") == 124
