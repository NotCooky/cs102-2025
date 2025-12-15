from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(n_rows: int = 15, n_cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * n_cols for _ in range(n_rows)]


def remove_wall(
    maze_grid: List[List[Union[str, int]]], cell_pos: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    row_idx, col_idx = cell_pos
    last_col_index = len(maze_grid[0]) - 1
    wall_direction = choice(("upward", "rightward"))

    if wall_direction == "upward":
        if row_idx > 1:
            maze_grid[row_idx - 1][col_idx] = " "
        elif col_idx < last_col_index - 1:
            maze_grid[row_idx][col_idx + 1] = " "
    else:
        if col_idx < last_col_index - 1:
            maze_grid[row_idx][col_idx + 1] = " "
        elif row_idx > 1:
            maze_grid[row_idx - 1][col_idx] = " "

    return maze_grid


def bin_tree_maze(
    n_rows: int = 15, n_cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    maze_grid = create_grid(n_rows, n_cols)
    free_cells = []

    for i, row in enumerate(maze_grid):
        for j, cell in enumerate(row):
            if i % 2 == 1 and j % 2 == 1:
                maze_grid[i][j] = " "
                free_cells.append((i, j))

    # Проходим по всем свободным клеткам и убираем стены
    for current_cell in free_cells:
        remove_wall(maze_grid, current_cell)

    # Размещение входа и выхода
    if random_exit:
        entrance_row, exit_row = randint(0, n_rows - 1), randint(0, n_rows - 1)
        entrance_col = (
            randint(0, n_cols - 1)
            if entrance_row in (0, n_rows - 1)
            else choice((0, n_cols - 1))
        )
        exit_col = (
            randint(0, n_cols - 1)
            if exit_row in (0, n_rows - 1)
            else choice((0, n_cols - 1))
        )
    else:
        entrance_row, entrance_col = 0, n_cols - 2
        exit_row, exit_col = n_rows - 1, 1

    maze_grid[entrance_row][entrance_col] = "X"
    maze_grid[exit_row][exit_col] = "X"

    return maze_grid


def get_exits(maze_grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exit_points = []
    for i in range(len(maze_grid)):
        for j in range(len(maze_grid[i])):
            if maze_grid[i][j] == "X":
                exit_points.append((i, j))
                if len(exit_points) == 2:
                    return exit_points
    return exit_points


def make_step(
    maze_grid: List[List[Union[str, int]]], step_num: int
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    total_rows = len(maze_grid)
    total_cols = len(maze_grid[0])
    next_step = step_num + 1

    for i in range(total_rows):
        for j in range(total_cols):
            if maze_grid[i][j] == step_num:
                adjacent_cells = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
                for cell_i, cell_j in adjacent_cells:
                    if (
                        0 <= cell_i < total_rows
                        and 0 <= cell_j < total_cols
                        and maze_grid[cell_i][cell_j] == 0
                    ):
                        maze_grid[cell_i][cell_j] = next_step

    return maze_grid


def shortest_path(
    maze_grid: List[List[Union[str, int]]], exit_point: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    total_rows = len(maze_grid)
    total_cols = len(maze_grid[0])

    curr_row, curr_col = exit_point
    curr_step = int(maze_grid[curr_row][curr_col])
    path = [(curr_row, curr_col)]

    while maze_grid[curr_row][curr_col] != 1:
        curr_step -= 1
        if curr_step < 1:
            break

        adjacent_cells = [
            (curr_row, curr_col + 1),
            (curr_row, curr_col - 1),
            (curr_row + 1, curr_col),
            (curr_row - 1, curr_col),
        ]

        for cell_i, cell_j in adjacent_cells:
            if (
                0 <= cell_i < total_rows
                and 0 <= cell_j < total_cols
                and maze_grid[cell_i][cell_j] == curr_step
            ):
                path.append((cell_i, cell_j))
                curr_row, curr_col = cell_i, cell_j
                break

    return path


def encircled_exit(
    maze_grid: List[List[Union[str, int]]], position: Tuple[int, int]
) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    total_rows = len(maze_grid)
    total_cols = len(maze_grid[0])
    pos_row, pos_col = position

    # Проверка углов
    if (pos_row == 0 or pos_row == total_rows - 1) and (
        pos_col == 0 or pos_col == total_cols - 1
    ):
        return True

    # Проверка границ
    if pos_row == 0 and maze_grid[pos_row + 1][pos_col] != " ":
        return True
    if pos_row == total_rows - 1 and maze_grid[pos_row - 1][pos_col] != " ":
        return True
    if pos_col == 0 and maze_grid[pos_row][pos_col + 1] != " ":
        return True
    if pos_col == total_cols - 1 and maze_grid[pos_row][pos_col - 1] != " ":
        return True

    return False


def solve_maze(
    maze_grid: List[List[Union[str, int]]],
) -> Tuple[
    List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
]:
    """

    :param grid:
    :return:
    """
    maze_copy = deepcopy(maze_grid)
    exit_points = get_exits(maze_copy)

    if len(exit_points) == 1:
        return maze_copy, exit_points[0]

    for exit_pos in exit_points:
        if encircled_exit(maze_copy, exit_pos):
            return maze_copy, None

    # Подготовка сетки для волнового алгоритма
    for i in range(len(maze_copy)):
        for j in range(len(maze_copy[0])):
            if maze_copy[i][j] == " ":
                maze_copy[i][j] = 0

    entrance_row, entrance_col = exit_points[0]
    maze_copy[entrance_row][entrance_col] = 1

    exit_row, exit_col = exit_points[1]
    maze_copy[exit_row][exit_col] = 0

    step_counter = 1
    while maze_copy[exit_row][exit_col] == 0:
        make_step(maze_copy, step_counter)
        step_counter += 1
        if step_counter > len(maze_copy) * len(maze_copy[0]):
            return maze_copy, None

    solution_path = shortest_path(maze_copy, (exit_row, exit_col))
    return maze_copy, solution_path


def add_path_to_grid(
    maze_grid: List[List[Union[str, int]]],
    path_points: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """
    if path_points:
        for i, row in enumerate(maze_grid):
            for j, cell in enumerate(row):
                if (i, j) in path_points:
                    maze_grid[i][j] = "X"
    return maze_grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
