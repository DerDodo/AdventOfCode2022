from typing import List

from util.file_util import read_input_file


def parse_input() -> List[List[int]]:
    lines = read_input_file(8)
    return list(map(lambda line: [int(char) for char in line], lines))


def visible_from_left(tree_matrix: List[List[int]]) -> List[List[bool]]:
    result: List[List[bool]] = list(map(lambda _line: list(map(lambda _: False, _line)), tree_matrix))
    for i in range(len(tree_matrix)):
        current_height = -1
        for j in range(len(tree_matrix[i])):
            if tree_matrix[i][j] > current_height:
                result[i][j] = True
                current_height = tree_matrix[i][j]
    return result


def visible_from_right(tree_matrix: List[List[int]]) -> List[List[bool]]:
    result: List[List[bool]] = list(map(lambda _line: list(map(lambda _: False, _line)), tree_matrix))
    for i in range(len(tree_matrix)):
        current_height = -1
        for j in reversed(range(len(tree_matrix[i]))):
            if tree_matrix[i][j] > current_height:
                result[i][j] = True
                current_height = tree_matrix[i][j]
    return result


def visible_from_top(tree_matrix: List[List[int]]) -> List[List[bool]]:
    result: List[List[bool]] = list(map(lambda _line: list(map(lambda _: False, _line)), tree_matrix))
    for j in range(len(tree_matrix[0])):
        current_height = -1
        for i in range(len(tree_matrix)):
            if tree_matrix[i][j] > current_height:
                result[i][j] = True
                current_height = tree_matrix[i][j]
    return result


def visible_from_bottom(tree_matrix: List[List[int]]) -> List[List[bool]]:
    result: List[List[bool]] = list(map(lambda _line: list(map(lambda _: False, _line)), tree_matrix))
    for j in range(len(tree_matrix[0])):
        current_height = -1
        for i in reversed(range(len(tree_matrix))):
            if tree_matrix[i][j] > current_height:
                result[i][j] = True
                current_height = tree_matrix[i][j]
    return result


def level8_1() -> int:
    trees = parse_input()
    from_left = visible_from_left(trees)
    from_right = visible_from_right(trees)
    from_top = visible_from_top(trees)
    from_bottom = visible_from_bottom(trees)

    num_visible_trees = 0
    visible_trees = []
    for y in range(len(trees)):
        visible_trees_line = ""
        for x in range(len(trees[y])):
            is_visible = (from_left[y][x] or from_right[y][x] or from_top[y][x] or from_bottom[y][x])
            visible_trees_line += str(1) if is_visible else str(0)
            if is_visible:
                num_visible_trees += 1
        visible_trees.append(visible_trees_line)
    return num_visible_trees


if __name__ == '__main__':
    _num_visible_trees = level8_1()
    print(f"Num visible trees: {_num_visible_trees}")
