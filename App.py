import pygame
from AStarSearch import *
from Settings import *
from Grid import Grid


class App:
    def __init__(self):
        self.start = None
        self.goal = None
        self.ready = False
        self.searched = False
        self.grid = Grid(ROW_NUM, COL_NUM)
        self.path = []
        pygame.init()
        # Set the HEIGHT and WIDTH of the self.screen
        self.window_size = [int(25.5 * COL_NUM), int(25.5 * ROW_NUM + 100)]
        self.screen = pygame.display.set_mode(self.window_size)
        # Set title of self.screen
        pygame.display.set_caption("A* Search Algorithm Visualization")
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def run(self):
        # Loop until the user clicks the close button.
        done = False
        # -------- Main Program Loop -----------
        while not done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.ready = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT\
                        and self.get_cell(pygame.mouse.get_pos())[0] < ROW_NUM\
                        and self.get_cell(pygame.mouse.get_pos())[1] < COL_NUM:
                    if not self.start:
                        cell = self.get_cell(pygame.mouse.get_pos())
                        if not self.grid.is_obstacle(cell):
                            self.start = cell
                            self.grid.set_color(self.start, RED)
                    elif not self.goal:
                        cell = self.get_cell(pygame.mouse.get_pos())
                        if not self.grid.is_obstacle(cell):
                            self.goal = cell
                            self.grid.set_color(self.goal, GREEN)
                    elif not self.ready:
                        cell = self.get_cell(pygame.mouse.get_pos())
                        self.grid.set_color(cell, BLACK)
                        self.grid.set_obstacle(cell)
            # Set the screen background
            self.screen.fill(BLACK)
            self.button("Clear", (self.window_size[0] - 300) / 2, self.window_size[1] - 100,
                        100, 50, GREY, WHITE, self.clean)
            self.button("Maze", (self.window_size[0] + 100) / 2, self.window_size[1] - 100,
                        100, 50, GREY, WHITE, self.draw_maze)
            # if obstacle, goal and starting point all set, find the shortest path through a* search
            if self.ready and not self.searched:
                self.path = a_star_search_visualize(self, self.grid, self.start, self.goal)
                self.searched = True
            for item in self.path:
                if item != self.start and item != self.goal:
                    self.grid.set_color(item, DARK_BLUE)
            self.draw_graph(FAST)

        pygame.quit()
        quit()

    def draw_maze(self):
        self.clean()
        for i in range(ROW_NUM):
            self.grid.set_obstacle((i, 0))
            self.grid.set_obstacle((i, COL_NUM - 1))
        for i in range(COL_NUM):
            self.grid.set_obstacle((0, i))
            self.grid.set_obstacle((ROW_NUM - 1, i))
        recursive_maze_generation(self, 0, ROW_NUM - 1, 0, COL_NUM - 1)

    def get_cell(self, pos):
        # Change the x/y screen coordinates to grid coordinates
        col = pos[0] // (CELL_WIDTH + MARGIN)
        row = pos[1] // (CELL_HEIGHT + MARGIN)
        return row, col

    def draw_graph(self, speed):
        # Draw the grid
        for row in range(ROW_NUM):
            for col in range(COL_NUM):
                color = self.grid.grid_color[row][col]
                pygame.draw.rect(self.screen,
                                 color,
                                 [(MARGIN + CELL_WIDTH) * col + MARGIN,
                                  (MARGIN + CELL_HEIGHT) * row + MARGIN,
                                  CELL_WIDTH,
                                  CELL_HEIGHT])
        self.clock.tick(speed)
        # update the screen with what we've drawn.
        pygame.display.flip()

    def intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(WHITE)
            large_text = pygame.font.Font('freesansbold.ttf', LARGE_TEXT_FONT)
            text_surf, text_rect = self.text_objects("A* Search Algorithm Visualization", large_text)
            text_rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4))
            self.screen.blit(text_surf, text_rect)
            self.button("GO!", (self.window_size[0] - 100) / 2, self.window_size[1] / 2,
                        100, 50, DARK_GREEN, GREEN, self.run)
            pygame.display.update()
            self.clock.tick(15)

    def text_objects(self, text, font):
        text_surface = font.render(text, True, BLACK)
        return text_surface, text_surface.get_rect()

    def clean(self):
        self.searched = False
        self.start = None
        self.goal = None
        self.ready = False
        self.grid = Grid(ROW_NUM, COL_NUM)
        self.path = []

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac, (x, y, w, h))

            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(self.screen, ic, (x, y, w, h))

        small_text = pygame.font.SysFont("comicsansms", SMALL_TEXT_FONT)
        text_surf, text_rect = self.text_objects(msg, small_text)
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(text_surf, text_rect)


if __name__ == "__main__":
    app = App()
    app.intro()
