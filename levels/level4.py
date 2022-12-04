from typing import List

from util.file_util import read_input_file


class Assignments:
    assignment_1_left: int
    assignment_1_right: int
    assignment_2_left: int
    assignment_2_right: int

    def __init__(self, assignment: str):
        assignment_parts = assignment.split(",")
        assignment_1 = assignment_parts[0].split("-")
        assignment_2 = assignment_parts[1].split("-")

        self.assignment_1_left = int(assignment_1[0])
        self.assignment_1_right = int(assignment_1[1])
        self.assignment_2_left = int(assignment_2[0])
        self.assignment_2_right = int(assignment_2[1])

    def does_fully_overlap(self) -> bool:
        is_1_in_2 = (self.assignment_2_left <= self.assignment_1_left
                     and self.assignment_2_right >= self.assignment_1_right)
        is_2_in_1 = (self.assignment_1_left <= self.assignment_2_left
                     and self.assignment_1_right >= self.assignment_2_right)
        return is_1_in_2 or is_2_in_1

    def does_partly_overlap(self) -> bool:
        is_1_before_2 = (self.assignment_1_left < self.assignment_2_left
                         and self.assignment_1_right < self.assignment_2_left)
        is_2_before_1 = (self.assignment_2_left < self.assignment_1_left
                         and self.assignment_2_right < self.assignment_1_left)
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
