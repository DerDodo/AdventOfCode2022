from typing import List, Tuple

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
    lines = read_input_file(4)
    all_assignments = list(map(Assignments, lines))
    return all_assignments


def level4() -> Tuple[int, int]:
    assignments = parse_input_file()
    num_full_overlaps = sum(1 if assignment.does_fully_overlap() else 0 for assignment in assignments)
    num_partly_overlaps = sum(1 if assignment.does_partly_overlap() else 0 for assignment in assignments)
    return num_full_overlaps, num_partly_overlaps


if __name__ == '__main__':
    _num_full_overlaps, _num_partly_overlaps = level4()
    print(f"Numbers of full overlaps: {_num_full_overlaps}")
    print(f"Numbers of partly overlaps: {_num_partly_overlaps}")
