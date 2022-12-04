from typing import List

from util.file_util import read_input_file


class Assignments:
    assignment1Left: int
    assignment1Right: int
    assignment2Left: int
    assignment2Right: int

    def __init__(self, assignment: str):
        assignment_parts = assignment.split(",")
        assignment1 = assignment_parts[0].split("-")
        assignment2 = assignment_parts[1].split("-")

        self.assignment1Left = int(assignment1[0])
        self.assignment1Right = int(assignment1[1])
        self.assignment2Left = int(assignment2[0])
        self.assignment2Right = int(assignment2[1])

    def does_fully_overlap(self) -> bool:
        is_1_in_2 = (self.assignment2Left <= self.assignment1Left and self.assignment2Right >= self.assignment1Right)
        is_2_in_1 = (self.assignment1Left <= self.assignment2Left and self.assignment1Right >= self.assignment2Right)
        return is_1_in_2 or is_2_in_1

    def does_partly_overlap(self) -> bool:
        is_1_before_2 = (self.assignment1Left < self.assignment2Left and self.assignment1Right < self.assignment2Left)
        is_2_before_1 = (self.assignment2Left < self.assignment1Left and self.assignment2Right < self.assignment1Left)
        return not is_1_before_2 and not is_2_before_1


def parse_input_file() -> List[Assignments]:
    lines = read_input_file(4, 1)
    all_assignments = list(map(Assignments, lines))
    return all_assignments


if __name__ == '__main__':
    assignments = parse_input_file()
    num_full_overlaps = sum(1 if assignment.does_fully_overlap() else 0 for assignment in assignments)
    print("Numbers of full overlaps: " + str(num_full_overlaps))

    num_partly_overlaps = sum(1 if assignment.does_partly_overlap() else 0 for assignment in assignments)
    print("Numbers of partly overlaps: " + str(num_partly_overlaps))
