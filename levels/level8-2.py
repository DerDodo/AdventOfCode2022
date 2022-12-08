from typing import List

from util.file_util import read_input_file


def parse_input() -> List[List[int]]:
    lines = read_input_file(8, 1)
    return list(map(lambda line: [int(char) for char in line], lines))


def sum_visible_to_top(tree_matrix: List[List[int]], y: int, x: int) -> int:
    if y == 0:
        return 0

    num_visible = 1
    check_y = y - 1
    current_height = tree_matrix[y][x]
    while check_y > 0 and current_height > tree_matrix[check_y][x]:
        num_visible += 1
        check_y -= 1
    return num_visible


def sum_visible_to_bottom(tree_matrix: List[List[int]], y: int, x: int) -> int:
    if y == len(tree_matrix) - 1:
        return 0

    num_visible = 1
    check_y = y + 1
    current_height = tree_matrix[y][x]
    while check_y < len(tree_matrix) - 1 and current_height > tree_matrix[check_y][x]:
        num_visible += 1
        check_y += 1
    return num_visible


def sum_visible_to_left(tree_matrix: List[List[int]], y: int, x: int) -> int:
    if x == 0:
        return 0

    num_visible = 1
    check_x = x - 1
    current_height = tree_matrix[y][x]
    while check_x > 0 and current_height > tree_matrix[y][check_x]:
        num_visible += 1
        check_x -= 1
    return num_visible


def sum_visible_to_right(tree_matrix: List[List[int]], y: int, x: int) -> int:
    if x == len(tree_matrix[y]) - 1:
        return 0

    num_visible = 1
    check_x = x + 1
    current_height = tree_matrix[y][x]
    while check_x < len(tree_matrix[y]) - 1 and current_height > tree_matrix[y][check_x]:
        num_visible += 1
        check_x += 1
    return num_visible


def calc_scenic_score(tree_matrix: List[List[int]], y: int, x: int) -> int:
    to_top = sum_visible_to_top(tree_matrix, y, x)
    to_bottom = sum_visible_to_bottom(tree_matrix, y, x)
    to_left = sum_visible_to_left(tree_matrix, y, x)
    to_right = sum_visible_to_right(tree_matrix, y, x)
    return to_top * to_bottom * to_left * to_right


def calc_scenic_scores(tree_matrix: List[List[int]]) -> List[List[int]]:
    result: List[List[int]] = []
    for i in range(len(tree_matrix)):
        line: List[int] = []
        for j in range(len(tree_matrix[i])):
            line.append(calc_scenic_score(tree_matrix, i, j))
        result.append(line)
    return result


if __name__ == '__main__':
    trees = parse_input()
    scenic_scores = calc_scenic_scores(trees)
    max_scenic_score = max(map(lambda line: max(line), scenic_scores))
    for scores in scenic_scores:
        print(",".join(map(lambda x: str(x), scores)))
    print(f"Max scenic score: {max_scenic_score}")
