from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = " "

    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))
    
    for cell in empty_cells:
        x, y = cell

        directions = []

        if x - 2 >= 1:
            directions.append("up")
        if y + 2 < cols - 1:
            directions.append("right")
        
        if directions:
            direction = choice(directions)

            if direction == "up":
                grid[x - 1][y] = " "
            elif direction == "right":
                grid[x][y + 1] = " "

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

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

    exits = []
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
    
    cells_with_k = []
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


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    x, y = exit_coord

    path = [(x, y)]
    k = grid[x][y]
    
    while k > 1:
        found = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny] == k - 1:
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
    
    if x > 0 and grid[x-1][y] == "■":  # сверху
        walls_around += 1
    if x < rows-1 and grid[x+1][y] == "■":  # снизу
        walls_around += 1
    if y > 0 and grid[x][y-1] == "■":  # слева
        walls_around += 1
    if y < cols-1 and grid[x][y+1] == "■":  # справа
        walls_around += 1
    
    if (x == 0 or x == rows-1) and (y == 0 or y == cols-1):
        return walls_around >= 2
    
    if x == 0 or x == rows-1 or y == 0 or y == cols-1:
        return walls_around >= 3
    
    return walls_around == 4


def solve_maze(grid: List[List[Union[str, int]]],) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
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
    while maze[end[0]][end[1]] == 0:
        make_step(maze, k)
        k += 1
        if k > len(maze) * len(maze[0]):
            return grid, None
    
    path = shortest_path(maze, end)

    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
