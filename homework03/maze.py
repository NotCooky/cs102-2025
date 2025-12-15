from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union, cast

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """
    grid = create_grid(rows, cols)
    
    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            grid[x][y] = " "
            
            directions: List[str] = []
            if x > 1:
                directions.append("up")
            if y < cols - 2:
                directions.append("right")
            
            if directions:
                direction = choice(directions)
                if direction == "up":
                    grid[x - 1][y] = " "
                elif direction == "right":
                    grid[x][y + 1] = " "

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """
    exits: List[Tuple[int, int]] = []
    rows = len(grid)
    cols = len(grid[0])

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == "X":
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])

    cells_with_k: List[Tuple[int, int]] = []
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == k:
                cells_with_k.append((x, y))

    for x, y in cells_with_k:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                cell_value = grid[nx][ny]
                if cell_value == 0 or cell_value == " " or cell_value == "X":
                    if cell_value == "X":
                        if grid[x][y] == 1:
                            grid[nx][ny] = 2
                        else:
                            grid[nx][ny] = k + 1
                    else:
                        grid[nx][ny] = k + 1
    return grid


def shortest_path(grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid:
    :param exit_coord:
    :return:
    """
    x, y = exit_coord
    
    # Проверяем, что значение в клетке - число
    if not isinstance(grid[x][y], int):
        return None
    
    k = cast(int, grid[x][y])
    
    if k <= 0:
        return None
    
    path: List[Tuple[int, int]] = [(x, y)]

    while k > 1:
        found = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                cell_value = grid[nx][ny]
                if isinstance(cell_value, int) and cell_value == k - 1:
                    path.append((nx, ny))
                    x, y = nx, ny
                    k -= 1
                    found = True
                    break

        if not found:
            return None

    path.reverse()
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    walls_around = 0

    if x > 0 and grid[x - 1][y] == "■":
        walls_around += 1
    if x < rows - 1 and grid[x + 1][y] == "■":
        walls_around += 1
    if y > 0 and grid[x][y - 1] == "■":
        walls_around += 1
    if y < cols - 1 and grid[x][y + 1] == "■":
        walls_around += 1

    if (x == 0 or x == rows - 1) and (y == 0 or y == cols - 1):
        return walls_around >= 2

    if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
        return walls_around >= 3

    return walls_around == 4


def solve_maze(grid: List[List[Union[str, int]]]) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    :param grid:
    :return:
    """
    maze = deepcopy(grid)
    exits = get_exits(maze)

    if len(exits) < 2:
        return grid, None if len(exits) == 0 else exits[0]

    start, end = exits[0], exits[1]

    if encircled_exit(maze, end):
        return grid, None

    # Инициализируем лабиринт для алгоритма Дейкстры
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x][y] == " ":
                maze[x][y] = 0

    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x][y] == "X":
                if (x, y) == start:
                    maze[x][y] = 1
                else:
                    maze[x][y] = 0

    k = 1
    max_steps = len(maze) * len(maze[0])
    end_value = maze[end[0]][end[1]]
    
    # Проверяем, что значение в конечной точке - число или "X"
    while (isinstance(end_value, int) and end_value == 0) or end_value == "X":
        make_step(maze, k)
        k += 1
        if k > max_steps:
            return grid, None
        end_value = maze[end[0]][end[1]]

    path = shortest_path(maze, end)
    return grid, path


def add_path_to_grid(grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param path:
    :return:
    """
    if path:
        if isinstance(path, tuple):  # Одна точка
            i, j = path
            grid[i][j] = "X"
        else:  # Список точек
            for i, j in path:
                grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))