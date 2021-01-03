import sys
import os
from pprint import pprint
from random import randrange

import pygame
COLORS = ["red", "blue", "black"]
left = 10
top = 10
maximum = (0, 0)
gold_block = (0, 0)


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
        self.boardpiece = [[]]
        self.players = ["red", "blue", "black"][:players]
        self.playerslive = self.players[::]
        self.hod = randrange(0, players)
        self.kolvo = players
        self.left = left
        self.top = top
        self.cell_size = tile_width
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] in ['6', '7', '8'] and self.kolvo == 2:
                    self.board[y][x] = '.'
                    self.boardpiece[y] += [None]
                if self.board[y][x] == 'x':
                    self.boardpiece[y] += [None]
                    Tile("none", x, y)
                elif self.board[y][x] == '@':
                    Tile("gold", x, y)
                    global gold_block
                    gold_block = (x, y)
                    self.boardpiece[y] += [None]
                elif self.board[y][x] == '.':
                    self.boardpiece[y] += [None]
                    Tile("empty", x, y)
                elif self.board[y][x] == '#':
                    self.boardpiece[y] += [None]
                    Tile("empty", x, y)
                    Tree(x, y)
                elif int(self.board[y][x]) % 3 == 0:
                    Tile("empty", x, y)
                    self.boardpiece[y] += [King(COLORS[(int(self.board[y][x])) // 3], x, y)]
                elif int(self.board[y][x]) % 3 == 1:
                    Tile("empty", x, y)
                    self.boardpiece[y] += [Rook(COLORS[(int(self.board[y][x])) // 3], x, y)]
                elif int(self.board[y][x]) % 3 == 2:
                    Tile("empty", x, y)
                    self.boardpiece[y] += [Bishop(COLORS[(int(self.board[y][x])) // 3], x, y)]
            self.boardpiece += [[]]

    def render(self):
        '''for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(screen, "white", (left + i * self.cell_size,
                                                   top + j * self.cell_size,
                                                   self.cell_size,
                                                   self.cell_size), width=1)'''
        pygame.draw.rect(screen, "black", (left,
                                           top,
                                           self.cell_size * len(self.board),
                                           self.cell_size * len(self.board[0])), width=2)

        for cell in kill_cells:
            pygame.draw.line(screen, "red",
                             (self.left + cell[0] * self.cell_size + 3,
                              self.top + cell[1] * self.cell_size + 4),
                             (self.left + cell[0] * self.cell_size + self.cell_size - 5,
                              self.top + cell[1] * self.cell_size + self.cell_size - 4), 2)

            pygame.draw.line(screen, "red",
                             (self.left + cell[0] * self.cell_size + 3,
                              self.top + cell[1] * self.cell_size + self.cell_size - 3),
                             (self.left + cell[0] * self.cell_size + self.cell_size - 4,
                              self.top + cell[1] * self.cell_size + 4), 2)

        for cell in move_cells:
            pygame.draw.circle(screen, "green",
                               (self.left + cell[0] * self.cell_size + self.cell_size // 2,
                                self.top + cell[1] * self.cell_size + self.cell_size // 2),
                               self.cell_size // 2 - 3, 2)

        pygame.draw.rect(screen, "red", (self.left + selected_cell[0] * self.cell_size,
                                         self.top + selected_cell[1] * self.cell_size,
                                         self.cell_size,
                                         self.cell_size), width=1)
        if chosen_cell:
            pygame.draw.rect(screen, "green", (self.left + chosen_cell[0] * self.cell_size + 1,
                                               self.top + chosen_cell[1] * self.cell_size + 1,
                                               self.cell_size - 2,
                                               self.cell_size - 2), width=1)

    def get_click(self, pos):
        cell = self.get_cell(pos)
        global selected_cell
        if not (cell is None or self.board[cell[0]][cell[1]] == 'x'):
            selected_cell = list(cell)

    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if -1 < x < len(self.board) and -1 < y < len(self.board[0]):
            return x, y
        return None

    def moved_cells(self):
        return self.boardpiece[chosen_cell[1]][chosen_cell[0]].can_move()

    def move_piece(self):
        global chosen_cell, move_cells, kill_cells, game_over, selecting_kill
        self.kill(selected_cell)

        if selected_cell[1] == gold_block[1] and selected_cell[0] == gold_block[0] and\
                not self.boardpiece[chosen_cell[1]][chosen_cell[0]].wasongold:
            if type(self.boardpiece[chosen_cell[1]][chosen_cell[0]]) is King:
                game_over = True
                self.playerslive = [self.boardpiece[chosen_cell[1]][chosen_cell[0]].color]
            else:
                self.boardpiece[chosen_cell[1]][chosen_cell[0]].wasongold = True
                selecting_kill = True

        f = self.board[chosen_cell[1]][chosen_cell[0]]
        self.board[chosen_cell[1]][chosen_cell[0]] = '.'
        if chosen_cell[1] == gold_block[1] and chosen_cell[0] == gold_block[0]:
            self.board[chosen_cell[1]][chosen_cell[0]] = '@'
        self.board[selected_cell[1]][selected_cell[0]] = f

        self.boardpiece[chosen_cell[1]][chosen_cell[0]].x = selected_cell[0]
        self.boardpiece[chosen_cell[1]][chosen_cell[0]].y = selected_cell[1]
        self.boardpiece[selected_cell[1]][selected_cell[0]] = self.boardpiece[chosen_cell[1]][chosen_cell[0]]
        self.boardpiece[chosen_cell[1]][chosen_cell[0]].move()
        self.boardpiece[chosen_cell[1]][chosen_cell[0]] = None
        if not selecting_kill:
            self.hod = (self.hod + 1) % len(self.playerslive)
        chosen_cell = False
        move_cells = []
        kill_cells = []
        if len(self.playerslive) == 1:
            game_over = True
        # pprint(self.board)
        # print("===========")
        '''for i in range(len(self.boardpiece)):
            for j in range(len(self.boardpiece[i])):
                if self.boardpiece[i][j] is None:
                    print("N", end=' ')
                elif type(self.boardpiece[i][j]) is Rook:
                    print("R", end=' ')
                elif type(self.boardpiece[i][j]) is Bishop:
                    print("B", end=' ')
                elif type(self.boardpiece[i][j]) is King:
                    print("K", end=' ')
            print()
        print("==============\n")'''

    def kill(self, cell):
        if self.boardpiece[cell[1]][cell[0]] is None:
            return

        if type(self.boardpiece[selected_cell[1]][selected_cell[0]]) is King:
            if self.boardpiece[selected_cell[1]][selected_cell[0]].color == "red":
                del self.playerslive[self.playerslive.index("red")]
                for sprite in red_piece_sprites:
                    self.boardpiece[sprite.y][sprite.x] = None
                    self.board[sprite.y][sprite.x] = '.'
                    sprite.kill()
            elif self.boardpiece[selected_cell[1]][selected_cell[0]].color == "blue":
                del self.playerslive[self.playerslive.index("blue")]
                for sprite in blue_piece_sprites:
                    self.boardpiece[sprite.y][sprite.x] = None
                    self.board[sprite.y][sprite.x] = '.'
                    sprite.kill()
            elif self.boardpiece[selected_cell[1]][selected_cell[0]].color == "black":
                del self.playerslive[self.playerslive.index("black")]
                for sprite in black_piece_sprites:
                    self.boardpiece[sprite.y][sprite.x] = None
                    self.board[sprite.y][sprite.x] = '.'
                    sprite.kill()
            self.hod = self.playerslive.index(self.boardpiece[chosen_cell[1]][chosen_cell[0]].color)
        else:
            self.boardpiece[cell[1]][cell[0]].kill()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(all_sprites, tile_sprites)
        global tile_images
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * x + left, tile_height * y + top)


class Piece(pygame.sprite.Sprite):
    def __init__(self, color, x, y, tree=False):
        """Общая форма создания фигур,
        color - цвет,
        (x, y) - координаты фигуры на поле"""
        if color == "red":
            super().__init__(all_sprites, piece_sprites, red_piece_sprites)
        elif color == "blue":
            super().__init__(all_sprites, piece_sprites, blue_piece_sprites)
        elif color == "black":
            super().__init__(all_sprites, piece_sprites, black_piece_sprites)
        self.tree = tree
        self.color = color
        self.wasongold = False
        self.numcolor = COLORS.index(self.color)
        self.x = x
        self.y = y

    def can_move_like_rook(self):
        move_cells = []
        kill_cells = []
        if chosen_cell[1] - 1 >= 0:
            if board.board[chosen_cell[1] - 1][chosen_cell[0]].isdigit() and\
                    int(board.board[chosen_cell[1] - 1][chosen_cell[0]]) // 3 != self.numcolor:
                kill_cells += [[chosen_cell[0], chosen_cell[1] - 1]]
            elif board.board[chosen_cell[1] - 1][chosen_cell[0]] in ["@", "."]:
                move_cells += [[chosen_cell[0], chosen_cell[1] - 1]]

        if chosen_cell[0] - 1 >= 0:
            if board.board[chosen_cell[1]][chosen_cell[0] - 1].isdigit() and\
                    int(board.board[chosen_cell[1]][chosen_cell[0] - 1]) // 3 != self.numcolor:
                kill_cells += [[chosen_cell[0] - 1, chosen_cell[1]]]
            elif board.board[chosen_cell[1]][chosen_cell[0] - 1] in ["@", "."]:
                move_cells += [[chosen_cell[0] - 1, chosen_cell[1]]]

        if chosen_cell[0] + 1 <= maximum[0]:
            if board.board[chosen_cell[1]][chosen_cell[0] + 1].isdigit() and\
                    int(board.board[chosen_cell[1]][chosen_cell[0] + 1]) // 3 != self.numcolor:
                kill_cells += [[chosen_cell[0] + 1, chosen_cell[1]]]
            elif board.board[chosen_cell[1]][chosen_cell[0] + 1] in ["@", "."]:
                move_cells += [[chosen_cell[0] + 1, chosen_cell[1]]]

        if chosen_cell[1] + 1 <= maximum[1]:
            if board.board[chosen_cell[1] + 1][chosen_cell[0]].isdigit() and\
                    int(board.board[chosen_cell[1] + 1][chosen_cell[0]]) // 3 != self.numcolor:
                kill_cells += [[chosen_cell[0], chosen_cell[1] + 1]]
            elif board.board[chosen_cell[1] + 1][chosen_cell[0]] in ["@", "."]:
                move_cells += [[chosen_cell[0], chosen_cell[1] + 1]]
        return move_cells, kill_cells

    def can_move_like_bishop(self):
        move_cells = []
        kill_cells = []
        if chosen_cell[1] - 1 >= 0 and chosen_cell[0] - 1 >= 0:
            if board.board[chosen_cell[1] - 1][chosen_cell[0] - 1].isdigit() and\
                    int(board.board[chosen_cell[1] - 1][chosen_cell[0] - 1]) // 3 != self.numcolor:
                kill_cells += [[chosen_cell[0] - 1, chosen_cell[1] - 1]]
            elif board.board[chosen_cell[1] - 1][chosen_cell[0] - 1] in ["@", "."]:
                move_cells += [[chosen_cell[0] - 1, chosen_cell[1] - 1]]

        if chosen_cell[1] - 1 >= 0 and chosen_cell[0] + 1 <= maximum[0]:
            if board.board[chosen_cell[1] - 1][chosen_cell[0] + 1].isdigit() and \
                    int(board.board[chosen_cell[1] - 1][chosen_cell[0] + 1]) // 3 != self.numcolor:
                kill_cells += [[chosen_cell[0] + 1, chosen_cell[1] - 1]]
            elif board.board[chosen_cell[1] - 1][chosen_cell[0] + 1] in ["@", "."]:
                move_cells += [[chosen_cell[0] + 1, chosen_cell[1] - 1]]

        if chosen_cell[1] + 1 <= maximum[1] and chosen_cell[0] - 1 >= 0:
            if board.board[chosen_cell[1] + 1][chosen_cell[0] - 1].isdigit() and \
                    int(board.board[chosen_cell[1] + 1][chosen_cell[0] - 1]) // 3 != self.numcolor:
                kill_cells += [[chosen_cell[0] - 1, chosen_cell[1] + 1]]
            elif board.board[chosen_cell[1] + 1][chosen_cell[0] - 1] in ["@", "."]:
                move_cells += [[chosen_cell[0] - 1, chosen_cell[1] + 1]]

        if chosen_cell[1] + 1 <= maximum[1] and chosen_cell[0] + 1 <= maximum[0]:
            if board.board[chosen_cell[1] + 1][chosen_cell[0] + 1].isdigit() and \
                    int(board.board[chosen_cell[1] + 1][chosen_cell[0] + 1]) // 3 != self.numcolor:
                kill_cells += [[chosen_cell[0] + 1, chosen_cell[1] + 1]]
            elif board.board[chosen_cell[1] + 1][chosen_cell[0] + 1] in ["@", "."]:
                move_cells += [[chosen_cell[0] + 1, chosen_cell[1] + 1]]
        return move_cells, kill_cells

    def move(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top)


class King(Piece):
    def __init__(self, color, x, y, tree=False):
        super().__init__(color, x, y, tree)
        imagename = "king_" + self.color + ".png"
        self.image = load_image(imagename)
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top)

    def can_move(self):
        move_cells1, kill_cells1 = self.can_move_like_bishop()
        move_cells2, kill_cells2 = self.can_move_like_rook()
        return move_cells1 + move_cells2, kill_cells1 + kill_cells2


class Rook(Piece):
    def __init__(self, color, x, y, tree=False):
        super().__init__(color, x, y, tree)
        imagename = "rook_" + self.color + ".png"
        self.image = load_image(imagename)
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top)

    def can_move(self):
        move_cells, kill_cells = self.can_move_like_rook()
        return move_cells, kill_cells


class Bishop(Piece):
    def __init__(self, color, x, y, tree=False):
        super().__init__(color, x, y, tree)
        imagename = "bishop_" + self.color + ".png"
        self.image = load_image(imagename)
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top)

    def can_move(self):
        move_cells, kill_cells = self.can_move_like_bishop()
        return move_cells, kill_cells


class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, other_sprites)
        self.x = x
        self.y = y
        self.image = load_image("tree.png")
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top)


class KillImage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, other_sprites)
        self.x = x
        self.y = y
        self.image = load_image("kill.png")
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top)


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
pygame.joystick.init()

tile_width = tile_height = 30
size = width, height = 400, 400
screen = pygame.display.set_mode(size)

tile_images = {
    'gold': load_image('gold.png'),
    'empty': load_image('grass.png'),
    'none': load_image('none.png')
}

all_sprites = pygame.sprite.Group()
tile_sprites = pygame.sprite.Group()
piece_sprites = pygame.sprite.Group()
other_sprites = pygame.sprite.Group()

red_piece_sprites = pygame.sprite.Group()
blue_piece_sprites = pygame.sprite.Group()
black_piece_sprites = pygame.sprite.Group()

level = load_level("map1.txt")
selected_cell = list(map(lambda x: x // 2 + 1, maximum))
board = Board(level, 2)
# board.hod = 1
generate_level(level)
chosen_cell = False
selecting_kill = False
game_over = False
move_cells = []
kill_cells = []
killingimage = None

running = True
while running:
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN or
                event.type == pygame.MOUSEBUTTONDOWN or
        event.type == pygame.JOYAXISMOTION or
        event.type == pygame.JOYHATMOTION or
        event.type == pygame.JOYBUTTONDOWN) and game_over:
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
        if not selecting_kill and\
                ((event.type == pygame.JOYBUTTONDOWN and event.button == 1) or
                 (event.type == pygame.KEYDOWN and event.key in [13, 32])):
            if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and\
                    board.boardpiece[selected_cell[1]][selected_cell[0]].color == board.playerslive[board.hod]:
                chosen_cell = selected_cell[::]
                move_cells, kill_cells = board.moved_cells()
            elif selected_cell in move_cells or selected_cell in kill_cells:
                board.move_piece()

        if selecting_kill and\
                ((event.type == pygame.JOYBUTTONDOWN and event.button == 1) or
                 (event.type == pygame.KEYDOWN and event.key in [13, 32])):
            if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and\
                    board.boardpiece[selected_cell[1]][selected_cell[0]].color != board.playerslive[board.hod] and\
                    not (type(board.boardpiece[selected_cell[1]][selected_cell[0]]) is King):
                board.kill(selected_cell)
                selecting_kill = False
                board.hod = (board.hod + 1) % len(board.playerslive)
                if not (killingimage is None):
                    killingimage.kill()
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont("Bauhaus 93", 30)
    if game_over:
        text = "Player " + str(board.playerslive[board.hod]) + " win"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, 310))
        text = "Press any key to continue"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, 350))
    elif selecting_kill:
        text = "Player " + str(board.playerslive[board.hod])
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, 310))
        text = "Select piece to kill"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, 350))
        if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and\
                board.boardpiece[selected_cell[1]][selected_cell[0]].color != board.playerslive[board.hod] and \
                not (type(board.boardpiece[selected_cell[1]][selected_cell[0]]) is King):
            if not (killingimage is None):
                killingimage.kill()
            killingimage = KillImage(selected_cell[0], selected_cell[1])
        elif not (killingimage is None):
            killingimage.kill()
    else:
        text = "Player " + str(board.playerslive[board.hod]) + " move"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, 350))
    tile_sprites.draw(screen)
    piece_sprites.draw(screen)
    other_sprites.draw(screen)
    board.render()
    pygame.display.flip()
terminate()
