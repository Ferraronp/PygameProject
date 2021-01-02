import sys
import os
from pprint import pprint
import pygame
COLORS = ["red", "blue", "black"]
left = 10
top = 10
maximum = (0, 0)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    """Загрузка уровня из папки data и названия filename
    Возвращает двумерный массив с игровым полем
    x - клетки нет на поле
    . - пустая клетка
    @ - золотая клетка
    # - дерево
    0 + (i * 3) - король, i-ого цвета в списке
    1 + (i * 3) - ладья, i-ого цвета в списке
    2 + (i * 3) - слон, i-ого цвета в списке
    Список цветов [red, blue, black]"""
    filename = "data/" + filename
    if not os.path.isfile(filename):
        print(f"Файл с уровнем '{filename}' не найден")
        sys.exit()
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    global maximum
    maximum = (max_width - 1, len(level_map) - 1)

    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


class Board:
    def __init__(self, level, players):
        """players - количество игроков от 2 до 3"""
        self.board = level
        self.players = ["red", "blue", "black"][:players]
        self.hod = 0
        self.kolvo = players
        self.left = 10
        self.top = 10
        self.cell_size = tile_width
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] in ['7', '8', '9'] and players == 2:
                    self.board[y][x] = '.'
                if self.board[y][x] == 'x':
                    continue
                if self.board[y][x] == '@':
                    Tile("gold", x, y)
                elif self.board[y][x] == '.':
                    Tile("empty", x, y)
                elif self.board[y][x] == '#':
                    Tile("empty", x, y)
                    # Класс с деревом
                elif int(self.board[y][x]) % 3 == 0:
                    Tile("empty", x, y)
                    King(COLORS[(int(self.board[y][x])) // 3], x, y)
                elif int(self.board[y][x]) % 3 == 1:
                    Tile("empty", x, y)
                    Rook(COLORS[(int(self.board[y][x])) // 3], x, y)
                elif int(self.board[y][x]) % 3 == 2:
                    Tile("empty", x, y)
                    Bishop(COLORS[(int(self.board[y][x])) // 3], x, y)

    def render(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                '''pygame.draw.rect(screen, "white", (left + i * self.cell_size,
                                                   top + j * self.cell_size,
                                                   self.cell_size,
                                                   self.cell_size), width=1)'''
        pygame.draw.rect(screen, "red", (self.left + selected_cell[0] * self.cell_size,
                                           self.top + selected_cell[1] * self.cell_size,
                                           self.cell_size,
                                           self.cell_size), width=1)
        pygame.draw.rect(screen, "green", (self.left + chosen_cell[0] * self.cell_size,
                                         self.top + chosen_cell[1] * self.cell_size,
                                         self.cell_size,
                                         self.cell_size), width=1)

    def get_click(self, pos):
        cell = self.get_cell(pos)
        global selected_cell
        if cell is None:
            selected_cell = [0, 0]
        else:
            selected_cell = list(cell)

    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if -1 < x < len(self.board) and -1 < y < len(self.board[0]):
            return x, y
        return None


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(all_sprites)
        global tile_images
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * x + left, tile_height * y + top)


class Piece(pygame.sprite.Sprite):
    def __init__(self, color, x, y, tree=False):
        """Общая форма создания фигур,
        color - цвет,
        (x, y) - координаты фигуры на поле"""
        super().__init__(all_sprites)
        self.tree = tree
        self.color = color
        self.x = x
        self.y = y


class King(Piece):
    def __init__(self, color, x, y, tree=False):
        super().__init__(color, x, y, tree)
        self.image = load_image("king.png")
        self.rect = self.image.get_rect().move(
            tile_width * x + left, tile_height * y + top)


class Rook(Piece):
    def __init__(self, color, x, y, tree=False):
        super().__init__(color, x, y, tree)
        self.image = load_image("rook.png")
        self.rect = self.image.get_rect().move(
            tile_width * x + left, tile_height * y + top)


class Bishop(Piece):
    def __init__(self, color, x, y, tree=False):
        super().__init__(color, x, y, tree)
        self.image = load_image("bishop.png")
        self.rect = self.image.get_rect().move(
            tile_width * x + left, tile_height * y + top)


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('gold', x, y)


def check_selected_cell():
    res = True
    for i in range(2):
        if selected_cell[i] < 0:
            selected_cell[i] = 0
            res = False
        elif selected_cell[i] >= maximum[i]:
            selected_cell[i] = maximum[i]
            res = False
    return res


pygame.init()
pygame.font.init()

tile_width = tile_height = 30
size = width, height = 400, 400
screen = pygame.display.set_mode(size)

tile_images = {
    'gold': load_image('gold.png'),
    'empty': load_image('grass.png')
}

all_sprites = pygame.sprite.Group()
selected_cell = [0, 0]
level = load_level("map1.txt")
board = Board(level, 3)
generate_level(level)
chosen_cell = [-5, -5]

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
        if event.type == pygame.JOYHATMOTION:
            if joysticks[0].get_hat(0)[0] != 0 and joysticks[0].get_hat(0)[1] != 0:
                continue
            selected_cell[0] += joysticks[0].get_hat(0)[0]
            selected_cell[1] -= joysticks[0].get_hat(0)[1]
            if check_selected_cell():
                if level[selected_cell[0]][selected_cell[1]] == "x":
                    selected_cell[0] -= joysticks[0].get_hat(0)[0]
                    selected_cell[1] += joysticks[0].get_hat(0)[1]
        if event.type == pygame.KEYDOWN and (event.key == 100 or event.key == 1073741903):
            selected_cell[0] += 1
            if check_selected_cell():
                if level[selected_cell[0]][selected_cell[1]] == "x":
                    selected_cell[0] -= 1
        if event.type == pygame.KEYDOWN and (event.key == 97 or event.key == 1073741904):
            selected_cell[0] -= 1
            if check_selected_cell():
                if level[selected_cell[0]][selected_cell[1]] == "x":
                    selected_cell[0] += 1
        if event.type == pygame.KEYDOWN and (event.key == 115 or event.key == 1073741905):
            selected_cell[1] += 1
            if check_selected_cell():
                if level[selected_cell[0]][selected_cell[1]] == "x":
                    selected_cell[1] -= 1
        if event.type == pygame.KEYDOWN and (event.key == 119 or event.key == 1073741906):
            selected_cell[1] -= 1
            if check_selected_cell():
                if level[selected_cell[0]][selected_cell[1]] == "x":
                    selected_cell[1] += 1
        if ((event.type == pygame.JOYBUTTONDOWN and event.button == 0) or
                (event.type == pygame.KEYDOWN and event.key == 13)) and\
                level[selected_cell[0]][selected_cell[1]] != 'x':
            chosen_cell = selected_cell[::]
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    board.render()
    pygame.display.flip()
terminate()
