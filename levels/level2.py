from enum import IntEnum

from typing import List

from util.file_util import read_input_file


class Outcome(IntEnum):
    Victory = 6
    Draw = 3
    Loss = 0


class RPS(IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3

    def beats(self, other) -> Outcome:
        if ((self == RPS.Rock and other == RPS.Scissors) or
                (self == RPS.Paper and other == RPS.Rock) or
                (self == RPS.Scissors and other == RPS.Paper)):
            return Outcome.Victory
        elif self == other:
            return Outcome.Draw
        else:
            return Outcome.Loss


class Round:
    opponent: RPS
    you: RPS

    def __init__(self, opponent, you):
        self.opponent = opponent
        self.you = you

    def get_points(self) -> int:
        return self.you + self.you.beats(self.opponent)


def str2rps(text: str) -> RPS:
    if text == "A":
        return RPS.Rock
    elif text == "B":
        return RPS.Paper
    elif text == "C":
        return RPS.Scissors
    elif text == "X":
        return RPS.Rock
    elif text == "Y":
        return RPS.Paper
    elif text == "Z":
        return RPS.Scissors
    else:
        raise Exception("Cannot parse input: " + text)


def step1mapper(opponent: RPS, text: str) -> RPS:
    return str2rps(text)


step2map = {
    "X": {  # Loss
        RPS.Rock: RPS.Scissors,
        RPS.Paper: RPS.Rock,
        RPS.Scissors: RPS.Paper,
    },
    "Y": {  # Draw
        RPS.Rock: RPS.Rock,
        RPS.Paper: RPS.Paper,
        RPS.Scissors: RPS.Scissors,
    },
    "Z": {  # Win
        RPS.Rock: RPS.Paper,
        RPS.Paper: RPS.Scissors,
        RPS.Scissors: RPS.Rock,
    },
}


def step2mapper(opponent: RPS, text: str) -> RPS:
    return step2map[text][opponent]


def parse_input_file(mapper) -> List[Round]:
    lines = read_input_file(2, 1)
    all_rounds: List[Round] = list()
    for line in lines:
        parts = line.split(" ")
        opponent = str2rps(parts[0])
        you = mapper(opponent, parts[1])
        all_rounds.append(Round(opponent, you))
    return all_rounds


def calc_score(rounds: List[Round]) -> int:
    return sum(map(Round.get_points, rounds))


if __name__ == '__main__':
    rounds1 = parse_input_file(step1mapper)
    print("Total score round 1: " + str(calc_score(rounds1)))

    rounds2 = parse_input_file(step2mapper)
    print("Total score round 1: " + str(calc_score(rounds2)))
