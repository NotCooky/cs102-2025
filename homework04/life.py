import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cols for i in range(self.rows)]
        if randomize:
            for i, row in enumerate(grid):
                for j, _ in enumerate(row):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        row, col = cell
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    new_row = row + i
                    new_col = col + j
                    if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                        neighbours.append(self.curr_generation[new_row][new_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid(randomize=False)
        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                amount = sum(neighbours)
                if self.curr_generation[i][j] == 1 and 2 <= amount <= 3:
                    new_grid[i][j] = 1
                elif self.curr_generation[i][j] == 0 and amount == 3:
                    new_grid[i][j] = 1

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        if self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation != self.prev_generation:
            return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            grid = []
            for line in f:
                cleaned_line = line.strip()
                if cleaned_line:
                    row = [int(char) for char in cleaned_line]
                    grid.append(row)

        rows = len(grid)
        cols = len(grid[0])

        game = GameOfLife((rows, cols), randomize=False)

        game.curr_generation = grid

        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                row_as_string = "".join(str(x) for x in row)
                f.write(row_as_string + "\n")
