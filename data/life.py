import pygame
import sys


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, "white",
                                 (self.left + i * self.cell_size,
                                  self.top + j * self.cell_size,
                                  self.cell_size,
                                  self.cell_size),
                                 width=1)
                if self.board[j][i] == 1:
                    pygame.draw.rect(screen, (51, 255, 51),
                                     (self.left + i * self.cell_size + 1,
                                      self.top + j * self.cell_size + 1,
                                      self.cell_size - 2,
                                      self.cell_size - 2),
                                     width=0)

    def get_click(self, pos):
        cell = self.get_cell(pos)
        self.on_click(cell)

    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if -1 < x < self.width and -1 < y < self.height:
            return x, y
        return None

    def on_click(self, cell):
        if cell is None:
            return None
        if self.board[cell[1]][cell[0]] == 0:
            self.board[cell[1]][cell[0]] = 1
        else:
            self.board[cell[1]][cell[0]] = 0


class Life(Board):
    def next_move(self):
        sp = [[0] * self.width for _ in range(self.height)]
        for x in range(len(sp)):
            for y in range(len(sp[x])):
                i = self.get_neighbors(x, y)
                if self.board[x][y] == 0 and i == 3:
                    sp[x][y] = 1
                if self.board[x][y] == 1 and (i == 2 or i == 3):
                    sp[x][y] = 1
        self.board = sp[::]

    def get_neighbors(self, x, y):
        i = 0
        if x > 0 and y > 0:
            i += self.board[x - 1][y - 1]
        if y > 0:
            i += self.board[x][y - 1]
        if x < self.height - 1 and y > 0:
            i += self.board[x + 1][y - 1]
        if x > 0:
            i += self.board[x - 1][y]
        if x < self.height - 1:
            i += self.board[x + 1][y]
        if x > 0 and y < self.width - 1:
            i += self.board[x - 1][y + 1]
        if y < self.width - 1:
            i += self.board[x][y + 1]
        if x < self.height - 1 and y < self.width - 1:
            i += self.board[x + 1][y + 1]
        return i


def start():
    global screen
    pygame.init()
    board = Board(30, 31)
    life = Life(30, 31)
    life.board = board.board[::]
    board.set_view(10, 10, 15)
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    running = True
    time = 0
    MYEVENTTYPE = pygame.USEREVENT + 1
    font = pygame.font.Font(None, 20)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and time == 0 and event.button == 1:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == 32:
                if time != 0:
                    time = 0
                else:
                    time = 100
                pygame.time.set_timer(MYEVENTTYPE, time)
            if time != 0 and event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    time -= 5
                else:
                    time += 5
                if time < 5:
                    time = 5
                if time > 200:
                    time = 200
                pygame.time.set_timer(MYEVENTTYPE, time)
            if event.type == MYEVENTTYPE:
                life.next_move()
                board.board = life.board[::]
        screen.fill((0, 0, 0))
        board.render()
        text = "Space to start/stop. Use mouse wheel to speed up or slow down"
        string_rendered = font.render(text, 1, pygame.Color('yellow'))
        rect = string_rendered.get_rect()
        rect.y = height - 20
        rect.x = 10
        screen.blit(string_rendered, rect)
        pygame.display.flip()
    pygame.quit()
    sys.exit()
