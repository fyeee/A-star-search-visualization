import math
from Settings import *
import random


class Grid:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for __ in range(height)]
        self.grid_color = [[WHITE for _ in range(width)] for __ in range(height)]

    def set_obstacle(self, cell):
        row = cell[0]
        col = cell[1]
        self.grid[row][col] = 1
        self.set_color(cell, BLACK)

    def set_color(self, cell, color):
        row = cell[0]
        col = cell[1]
        self.grid_color[row][col] = color

    def clean_cell(self, cell):
        self.set_color(cell, WHITE)
        self.grid[cell[0]][cell[1]] = 0

    def get_color(self, cell):
        return self.grid_color[cell[0]][cell[1]]

    def is_obstacle(self, cell):
        row = cell[0]
        col = cell[1]
        return self.grid[row][col] == 1

    def neighbours(self, cell):
        row = cell[0]
        col = cell[1]
        south = east = north = west = False
        if not (0 <= row < self.height and 0 <= col < self.width):
            return []
        neighbours = []
        if row < self.height - 1 and not self.is_obstacle((row + 1, col)):
            neighbours.append((row + 1, col))
            south = True
        if row and not self.is_obstacle((row - 1, col)):
            neighbours.append((row - 1, col))
            north = True
        if col < self.width - 1 and not self.is_obstacle((row, col + 1)):
            neighbours.append((row, col + 1))
            east = True
        if col > 0 and not self.is_obstacle((row, col - 1)):
            neighbours.append((row, col - 1))
            west = True
        if south:
            if west and not self.is_obstacle((row + 1, col - 1)):
                neighbours.append((row + 1, col - 1))
            if east and not self.is_obstacle((row + 1, col + 1)):
                neighbours.append((row + 1, col + 1))
        if north:
            if west and not self.is_obstacle((row - 1, col - 1)):
                neighbours.append((row - 1, col - 1))
            if east and not self.is_obstacle((row - 1, col + 1)):
                neighbours.append((row - 1, col + 1))
        return neighbours

    def distance(self, x, y):
        return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

    def recursive_maze_generation(self, row_start, row_end, col_start, col_end):
        if row_start + 4 > row_end or col_start + 4 > col_end:
            return
        row_mid = (row_start + row_end) // 2
        col_mid = (col_start + col_end) // 2
        for i in range(col_start + 1, col_end):
            self.grid[row_mid][i] = 1
        for j in range(row_start + 1, row_end):
            self.grid[j][col_mid] = 1
        # rand1 = random.randrange(col_start + 1, col_mid, 1)
        # while rand
        self.grid[row_mid][random.randrange(col_start + 1, col_mid, 1)] = 0
        self.grid[row_mid][random.randrange(col_mid + 1, col_end)] = 0
        self.grid[random.randrange(row_start + 1, row_mid)][col_mid] = 0
        self.grid[random.randrange(row_mid + 1, row_end)][col_mid] = 0
        self.recursive_maze_generation(row_start, row_mid, col_start, col_mid)
        self.recursive_maze_generation(row_mid, row_end, col_start, col_mid)
        self.recursive_maze_generation(row_start, row_mid, col_mid, col_end)
        self.recursive_maze_generation(row_mid, row_end, col_mid, col_end)

    def __str__(self):
        result = ""
        for row in self.grid:
            result += str(row) + "\n"
        if result != "":
            result = result[:-1]
        return result


if __name__ == "__main__":
    grid = Grid(10, 10)
    print(grid)
    grid.set_obstacle((1, 1))
    print(grid.neighbours((0, 0)))
