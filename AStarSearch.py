from PriorityQueue import PriorityQueue
from Settings import *
import random


def heuristic(x, y):
    return max(abs(y[0] - x[0]), abs(y[1] - x[1]))


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def recursive_maze_generation(app, row_start, row_end, col_start, col_end):
    grid = app.grid
    if row_start + 4 > row_end or col_start + 4 > col_end:
        return
    row_mid = (row_start + row_end) // 2
    col_mid = (col_start + col_end) // 2
    rand = random.randrange(1, 5)
    rand1 = random.randrange(col_start + 1, col_mid, 2)
    rand2 = random.randrange(col_mid + 1, col_end, 2)
    rand3 = random.randrange(row_start + 1, row_mid, 2)
    rand4 = random.randrange(row_mid + 1, row_end, 2)
    for i in range(col_start + 1, col_end):
        if not (i == rand1 or i == rand2):
            grid.set_obstacle((row_mid, i))
    for j in range(row_start + 1, row_end):
        if not (j == rand3 or j == rand4):
            grid.set_obstacle((j, col_mid))
    if rand == 1:
        grid.set_obstacle((row_mid, rand1))
    elif rand == 2:
        grid.set_obstacle((row_mid, rand2))
    elif rand == 3:
        grid.set_obstacle((rand3, col_mid))
    else:
        grid.set_obstacle((rand4, col_mid))
    recursive_maze_generation(app, row_start, row_mid, col_start, col_mid)
    recursive_maze_generation(app, row_mid, row_end, col_start, col_mid)
    recursive_maze_generation(app, row_start, row_mid, col_mid, col_end)
    recursive_maze_generation(app, row_mid, row_end, col_mid, col_end)
    app.draw_graph(SLOW)


def a_star_search_visualize(app, grid, start, goal):
    frontier = PriorityQueue()
    frontier.add(start, 0)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while not frontier.is_empty():
        current = frontier.pop()
        if current == goal:
            return reconstruct_path(came_from, current)
        for neighbour in grid.neighbours(current):
            tentative_g_score = g_score[current] + grid.distance(current, neighbour)
            if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + heuristic(neighbour, goal)
                if not frontier.exist(neighbour):
                    frontier.add(neighbour, f_score[neighbour])
        for item in frontier.get_queue():
            if item != goal and app.grid.get_color(item) != BLUE:
                app.grid.set_color(item, SKY_BLUE)
        if current != start:
            app.grid.set_color(current, BLUE)
        app.draw_graph(FAST)
    return []
