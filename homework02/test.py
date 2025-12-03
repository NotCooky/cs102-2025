import pathlib
import typing as tp
T = tp.TypeVar("T")

def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    res = []
    for i in range(0, len(values), n):
        res.append(values[i:i+n])
    return res

a = [1, 2, 3, 4]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row = pos[0]
    return grid[row]



def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = pos[1]
    res = []
    for sublist in grid:
        res.append(sublist[col])
    return res

def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    pos_row, pos_col = pos
    n = len(grid)
    box_size = int(n**0.5)

    box_row = pos_row // box_size
    box_col = pos_col // box_size

    start_row = box_row * box_size
    start_col = box_col * box_size

    square = []
    for i in range(start_row, start_row + box_size):
        for j in range(start_col, start_col + box_size):
            square.append(grid[i][j])

    return square


a = [['5', '3', '.', '.', '7', '.', '.', '.', '.'],
 ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
 ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
 ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
 ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
 ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
 ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
 ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
 ['.', '.', '.', '.', '8', '.', '.', '7', '9']]



def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == '.':
                return (row_idx, col_idx)
            

def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    row_vals = get_row(grid, pos)
    col_vals = get_col(grid, pos)
    block_vals = get_block(grid, pos)

    all_used = set(row_vals) | set(col_vals) | set(block_vals)
    all_used.discard('.')
    numbers = {str(i) for i in range(1, 10)}
    possible = numbers - all_used
    return possible



def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    empty_pos = find_empty_positions(grid)
    if not empty_pos:
        return grid
    possible_answers = find_possible_values(grid, empty_pos)
    for answer in possible_answers:
        row, col = empty_pos
        grid[row][col] = answer
        result = solve(grid)
        if result:
            return result
        grid[row][col] = '.' # ok so if we got here then that value didnt work
    pass

print(solve(a))