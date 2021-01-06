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


code = "IDDQD"
i = 0


class Board:
    def __init__(self, players):
        """players - количество игроков от 2 до 3"""
        # self.board = level
        self.boardpiece = [[]]
        self.players = ["red", "blue", "black"][:players]
        self.playerslive = self.players[::]
        self.hod = randrange(0, players)
        self.kolvo = players
        self.left = left
        self.top = top
        self.cell_size = tile_width

    def render(self):
        pygame.draw.rect(screen, "black", (left,
                                           top,
                                           self.cell_size * len(self.boardpiece[0]),
                                           self.cell_size * len(self.boardpiece)), width=2)

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

        # Отрисовка линий между клеток
        '''for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        pygame.draw.rect(screen, "white", (left + i * self.cell_size,
                                                           top + j * self.cell_size,
                                                           self.cell_size,
                                                           self.cell_size), width=1)'''

    def get_click(self, pos):
        cell = self.get_cell(pos)
        global selected_cell
        if cell is not None and not level[cell[1]][cell[0]] == 'x':
            selected_cell = list(cell)

    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if -1 < x < len(self.boardpiece) and -1 < y < len(self.boardpiece[0]):
            return x, y
        return None

    def moved_cells(self):
        return self.boardpiece[chosen_cell[1]][chosen_cell[0]].can_move()

    def move_piece(self):
        global chosen_cell, move_cells, kill_cells, game_over, selecting_tree, was_on_gold
        self.kill(selected_cell)

        if selected_cell[1] == gold_block[1] and selected_cell[0] == gold_block[0] and\
                not was_on_gold[self.boardpiece[chosen_cell[1]][chosen_cell[0]].color]:
            if type(self.boardpiece[chosen_cell[1]][chosen_cell[0]]) is King:
                game_over = True
                self.playerslive = [self.boardpiece[chosen_cell[1]][chosen_cell[0]].color]
            else:
                was_on_gold[self.boardpiece[chosen_cell[1]][chosen_cell[0]].color] = True
                selecting_tree = True

        self.boardpiece[chosen_cell[1]][chosen_cell[0]].x = selected_cell[0]
        self.boardpiece[chosen_cell[1]][chosen_cell[0]].y = selected_cell[1]
        self.boardpiece[selected_cell[1]][selected_cell[0]] = self.boardpiece[chosen_cell[1]][chosen_cell[0]]
        self.boardpiece[chosen_cell[1]][chosen_cell[0]].move()
        self.boardpiece[chosen_cell[1]][chosen_cell[0]] = None
        if not selecting_tree:
            self.hod = (self.hod + 1) % len(self.playerslive)
        chosen_cell = False
        move_cells = []
        kill_cells = []
        if len(self.playerslive) == 1:
            game_over = True
        if game_over:
            clock.tick(1000)
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

        if type(self.boardpiece[cell[1]][cell[0]]) is King:
            if self.boardpiece[cell[1]][cell[0]].color == "red":
                del self.playerslive[self.playerslive.index("red")]
                for sprite in red_piece_sprites:
                    self.boardpiece[sprite.y][sprite.x] = None
                    level[sprite.y][sprite.x] = '.'
                    sprite.kill()
            elif self.boardpiece[cell[1]][cell[0]].color == "blue":
                del self.playerslive[self.playerslive.index("blue")]
                for sprite in blue_piece_sprites:
                    self.boardpiece[sprite.y][sprite.x] = None
                    level[sprite.y][sprite.x] = '.'
                    sprite.kill()
            elif self.boardpiece[cell[1]][cell[0]].color == "black":
                del self.playerslive[self.playerslive.index("black")]
                for sprite in black_piece_sprites:
                    self.boardpiece[sprite.y][sprite.x] = None
                    level[sprite.y][sprite.x] = '.'
                    sprite.kill()
            self.hod = self.playerslive.index(self.boardpiece[chosen_cell[1]][chosen_cell[0]].color)
        else:
            self.boardpiece[cell[1]][cell[0]].kill()
            self.boardpiece[cell[1]][cell[0]] = None


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
        self.numcolor = COLORS.index(self.color)
        self.x = x
        self.y = y
        imagename = type(self).__name__.lower() + "_" + self.color + ".png"
        self.image = load_image(imagename)
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top)

    def can_move_like_rook(self):
        move_cells = []
        kill_cells = []
        if chosen_cell[1] - 1 >= 0:
            if not board.boardpiece[chosen_cell[1] - 1][chosen_cell[0]] is None and\
                    board.boardpiece[chosen_cell[1] - 1][chosen_cell[0]].color != self.color and\
                    (not board.boardpiece[chosen_cell[1] - 1][chosen_cell[0]].tree or selecting_kill):
                kill_cells += [[chosen_cell[0], chosen_cell[1] - 1]]
            elif level[chosen_cell[1] - 1][chosen_cell[0]] in ["@", "."] and\
                    board.boardpiece[chosen_cell[1] - 1][chosen_cell[0]] is None:
                move_cells += [[chosen_cell[0], chosen_cell[1] - 1]]

        if chosen_cell[0] - 1 >= 0:
            if not board.boardpiece[chosen_cell[1]][chosen_cell[0] - 1] is None and\
                    board.boardpiece[chosen_cell[1]][chosen_cell[0] - 1].color != self.color and\
                    (not board.boardpiece[chosen_cell[1]][chosen_cell[0] - 1].tree or selecting_kill):
                kill_cells += [[chosen_cell[0] - 1, chosen_cell[1]]]
            elif level[chosen_cell[1]][chosen_cell[0] - 1] in ["@", "."] and\
                    board.boardpiece[chosen_cell[1]][chosen_cell[0] - 1] is None:
                move_cells += [[chosen_cell[0] - 1, chosen_cell[1]]]

        if chosen_cell[0] + 1 <= maximum[0]:
            if not board.boardpiece[chosen_cell[1]][chosen_cell[0] + 1] is None and\
                    board.boardpiece[chosen_cell[1]][chosen_cell[0] + 1].color != self.color and\
                    (not board.boardpiece[chosen_cell[1]][chosen_cell[0] + 1].tree or selecting_kill):
                kill_cells += [[chosen_cell[0] + 1, chosen_cell[1]]]
            elif level[chosen_cell[1]][chosen_cell[0] + 1] in ["@", "."] and\
                    board.boardpiece[chosen_cell[1]][chosen_cell[0] + 1] is None:
                move_cells += [[chosen_cell[0] + 1, chosen_cell[1]]]

        if chosen_cell[1] + 1 <= maximum[1]:
            if not board.boardpiece[chosen_cell[1] + 1][chosen_cell[0]] is None and\
                    board.boardpiece[chosen_cell[1] + 1][chosen_cell[0]].color != self.color and\
                    (not board.boardpiece[chosen_cell[1] + 1][chosen_cell[0]].tree or selecting_kill):
                kill_cells += [[chosen_cell[0], chosen_cell[1] + 1]]
            elif level[chosen_cell[1] + 1][chosen_cell[0]] in ["@", "."] and\
                    board.boardpiece[chosen_cell[1] + 1][chosen_cell[0]] is None:
                move_cells += [[chosen_cell[0], chosen_cell[1] + 1]]
        return move_cells, kill_cells

    def can_move_like_bishop(self):
        move_cells = []
        kill_cells = []
        if chosen_cell[1] - 1 >= 0 and chosen_cell[0] - 1 >= 0:
            if not board.boardpiece[chosen_cell[1] - 1][chosen_cell[0] - 1] is None and\
                    board.boardpiece[chosen_cell[1] - 1][chosen_cell[0] - 1].color != self.color and\
                    (not board.boardpiece[chosen_cell[1] - 1][chosen_cell[0] - 1].tree or selecting_kill):
                kill_cells += [[chosen_cell[0] - 1, chosen_cell[1] - 1]]
            elif level[chosen_cell[1] - 1][chosen_cell[0] - 1] in ["@", "."] and\
                    board.boardpiece[chosen_cell[1] - 1][chosen_cell[0] - 1] is None:
                move_cells += [[chosen_cell[0] - 1, chosen_cell[1] - 1]]

        if chosen_cell[1] - 1 >= 0 and chosen_cell[0] + 1 <= maximum[0]:
            if not board.boardpiece[chosen_cell[1] - 1][chosen_cell[0] + 1] is None and\
                    board.boardpiece[chosen_cell[1] - 1][chosen_cell[0] + 1].color != self.color and\
                    (not board.boardpiece[chosen_cell[1] - 1][chosen_cell[0] + 1].tree or selecting_kill):
                kill_cells += [[chosen_cell[0] + 1, chosen_cell[1] - 1]]
            elif level[chosen_cell[1] - 1][chosen_cell[0] + 1] in ["@", "."] and\
                    board.boardpiece[chosen_cell[1] - 1][chosen_cell[0] + 1] is None:
                move_cells += [[chosen_cell[0] + 1, chosen_cell[1] - 1]]

        if chosen_cell[1] + 1 <= maximum[1] and chosen_cell[0] - 1 >= 0:
            if not board.boardpiece[chosen_cell[1] + 1][chosen_cell[0] - 1] is None and\
                    board.boardpiece[chosen_cell[1] + 1][chosen_cell[0] - 1].color != self.color and\
                    (not board.boardpiece[chosen_cell[1] + 1][chosen_cell[0] - 1].tree or selecting_kill):
                kill_cells += [[chosen_cell[0] - 1, chosen_cell[1] + 1]]
            elif level[chosen_cell[1] + 1][chosen_cell[0] - 1] in ["@", "."] and\
                    board.boardpiece[chosen_cell[1] + 1][chosen_cell[0] - 1] is None:
                move_cells += [[chosen_cell[0] - 1, chosen_cell[1] + 1]]

        if chosen_cell[1] + 1 <= maximum[1] and chosen_cell[0] + 1 <= maximum[0]:
            if not board.boardpiece[chosen_cell[1] + 1][chosen_cell[0] + 1] is None and\
                    board.boardpiece[chosen_cell[1] + 1][chosen_cell[0] + 1].color != self.color and\
                    (not board.boardpiece[chosen_cell[1] + 1][chosen_cell[0] + 1].tree or selecting_kill):
                kill_cells += [[chosen_cell[0] + 1, chosen_cell[1] + 1]]
            elif level[chosen_cell[1] + 1][chosen_cell[0] + 1] in ["@", "."] and\
                    board.boardpiece[chosen_cell[1] + 1][chosen_cell[0] + 1] is None:
                move_cells += [[chosen_cell[0] + 1, chosen_cell[1] + 1]]
        return move_cells, kill_cells

    def move(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top - (self.tree * 19))


class King(Piece):
    def can_move(self):
        move_cells1, kill_cells1 = self.can_move_like_bishop()
        move_cells2, kill_cells2 = self.can_move_like_rook()
        return move_cells1 + move_cells2, kill_cells1 + kill_cells2


class Rook(Piece):
    def can_move(self):
        move_cells, kill_cells = self.can_move_like_rook()
        return move_cells, kill_cells


class Bishop(Piece):
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

    def move(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top)


class SelectImage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, piece_sprites)
        self.x = x
        self.y = y
        self.image = load_image("chosing.png")
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top)


def generate_level():
    global level
    i = 1
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in ['6', '7', '8'] and board.kolvo == 2:
                level[y][x] = '.'
            if level[y][x] == 'x':
                board.boardpiece[y] += [None]
                Tile("none", x, y)
            elif level[y][x] == '@':
                Tile("gold", x, y)
                global gold_block
                gold_block = (x, y)
                board.boardpiece[y] += [None]
            elif level[y][x] == '.':
                board.boardpiece[y] += [None]
                Tile("empty" + str(i % 2 + 1), x, y)
            elif level[y][x] == '#':
                board.boardpiece[y] += [None]
                Tile("empty" + str(i % 2 + 1), x, y)
                Tree(x, y)
            elif int(level[y][x]) % 3 == 0:
                Tile("empty" + str(i % 2 + 1), x, y)
                board.boardpiece[y] += [King(COLORS[(int(level[y][x])) // 3], x, y)]
                level[y][x] = '.'
            elif int(level[y][x]) % 3 == 1:
                Tile("empty" + str(i % 2 + 1), x, y)
                board.boardpiece[y] += [Rook(COLORS[(int(level[y][x])) // 3], x, y)]
                level[y][x] = '.'
            elif int(level[y][x]) % 3 == 2:
                Tile("empty" + str(i % 2 + 1), x, y)
                board.boardpiece[y] += [Bishop(COLORS[(int(level[y][x])) // 3], x, y)]
                level[y][x] = '.'
            i += 1
        board.boardpiece += [[]]
    del board.boardpiece[-1]


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


def training():
    intro_text = ["Назад", "Далее"]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 25
    rects = []
    texts = []
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        intro_rect.left = text_coord + 10
        intro_rect.y = 550
        rects += [(pygame.draw.rect(screen, "blue", (text_coord - 10, intro_rect.y - 15, 150, 50), width=0), "exit")]
        text_coord += intro_rect.width
        screen.blit(string_rendered, intro_rect)
        texts += [(string_rendered, intro_rect)]
        text_coord += 250
    mousex, mousey = 0, 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, cmd in rects:
                    if rect.left <= event.pos[0] <= rect.left + rect.width and \
                            rect.top <= event.pos[1] <= rect.top + rect.height:
                        if cmd == "exit":
                            return
                        return cmd()
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
        fon = pygame.transform.scale(load_image('fon.png'), (width, height))
        screen.blit(fon, (0, 0))
        for i in range(len(rects)):
            if rects[i][0].left <= mousex <= rects[i][0].left + rects[i][0].width and \
                    rects[i][0].top <= mousey <= rects[i][0].top + rects[i][0].height:
                color = "red"
            else:
                color = "blue"
            pygame.draw.rect(screen, color, (rects[i][0].left, rects[i][0].top, rects[i][0].width, rects[i][0].height))
            screen.blit(*texts[i])
        pygame.display.flip()
        clock.tick(FPS)


def select_count_of_players():
    intro_text = [("2 игрока", "exit"),
                  ("3 игрока", "exit"),
                  ("Назад", start_screen)]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 10
    rects = []
    texts = []
    for line, i in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 50
        rects += [pygame.draw.rect(screen, "blue", (intro_rect.x - 15, text_coord - 15, 150, 50), width=0)]
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        texts += [(string_rendered, intro_rect)]
    mousex, mousey = 0, 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(rects)):
                    if rects[i].left <= event.pos[0] <= rects[i].left + rects[i].width and\
                            rects[i].top <= event.pos[1] <= rects[i].top + rects[i].height:
                        if intro_text[i][1] == "exit":
                            return i + 2
                        return intro_text[i][1]()
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
        for i in range(len(rects)):
            if rects[i].left <= mousex <= rects[i].left + rects[i].width and\
                    rects[i].top <= mousey <= rects[i].top + rects[i].height:
                color = "red"
            else:
                color = "blue"
            pygame.draw.rect(screen, color, (rects[i].left, rects[i].top, rects[i].width, rects[i].height))
            screen.blit(*texts[i])
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    egg = [4, 4, 6, 6, 7, 5, 7, 5, 13, 14, 3]
    intro_text = [("Начать игру", select_count_of_players),
                  ("Обучение", training)]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 10
    rects = []
    texts = []
    for line, cmd in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 50
        rects += [(pygame.draw.rect(screen, "blue", (intro_rect.x - 15, text_coord - 15, 150, 50), width=0), cmd)]
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        texts += [(string_rendered, intro_rect)]
    mousex, mousey = 0, 0
    f = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, cmd in rects:
                    if rect.left <= event.pos[0] <= rect.left + rect.width and\
                            rect.top <= event.pos[1] <= rect.top + rect.height:
                        if cmd == "exit":
                            return
                        return cmd()
            if event.type == pygame.JOYBUTTONDOWN:
                # print(event.button, f, egg[f])
                if event.button == egg[f]:
                    f += 1
                    if f == len(egg):
                        print("Hello, world")
                        j = sys.path[0]
                        sys.path[0] += '\\data'
                        import life
                        life.start()
                        sys.path[0] = j
                        egg = [-1]
                else:
                    f = 0
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
        for i in range(len(rects)):
            if rects[i][0].left <= mousex <= rects[i][0].left + rects[i][0].width and\
                    rects[i][0].top <= mousey <= rects[i][0].top + rects[i][0].height:
                color = "red"
            else:
                color = "blue"
            pygame.draw.rect(screen, color, (rects[i][0].left, rects[i][0].top, rects[i][0].width, rects[i][0].height))
            screen.blit(*texts[i])
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
pygame.font.init()
pygame.joystick.init()

FPS = 60
clock = pygame.time.Clock()
tile_width = tile_height = 50
size = width, height = tile_width * 9 + 50, tile_height * 9 + 150
screen = pygame.display.set_mode(size)

tile_images = {
    'gold': load_image('gold.png'),
    'empty1': load_image('grass1.png'),
    'empty2': load_image('grass2.png'),
    'none': load_image('none.png')
}

was_on_gold = {
    "red": False,
    "blue": False,
    "black": False
}

all_sprites = pygame.sprite.Group()
tile_sprites = pygame.sprite.Group()
piece_sprites = pygame.sprite.Group()
other_sprites = pygame.sprite.Group()

red_piece_sprites = pygame.sprite.Group()
blue_piece_sprites = pygame.sprite.Group()
black_piece_sprites = pygame.sprite.Group()


playerskolvo = 0
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
while playerskolvo == 0:
    playerskolvo = start_screen()
level = load_level("map" + str(playerskolvo) + "_" + str(randrange(1, 6)) + ".txt")
selected_cell = list(map(lambda x: x // 2 + 1, maximum))
board = Board(playerskolvo)

generate_level()
chosen_cell = False
selecting_kill = False
selecting_tree = False
moving_tree = False
game_over = False
move_cells = []
kill_cells = []
selectinging_image = None
running = True
while running:
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and\
            event.unicode == code[i] and chosen_cell and\
                len(code) == 5:
            i += 1
            if i == len(code) and\
                    level[chosen_cell[1]][chosen_cell[0]] != '@' and\
                    not selecting_kill and not selecting_tree and\
                    not moving_tree and not game_over:
                board.boardpiece[chosen_cell[1]][chosen_cell[0]].tree = True
                board.boardpiece[chosen_cell[1]][chosen_cell[0]].move()
                Tree(chosen_cell[0], chosen_cell[1])
                level[chosen_cell[1]][chosen_cell[0]] = "#"
                code += 'D'
                i = 0
            elif i == len(code):
                code += 'D'
                i = 0
        elif event.type == pygame.KEYDOWN:
            i = 0

        if (event.type == pygame.KEYDOWN or
                event.type == pygame.MOUSEBUTTONDOWN or
            event.type == pygame.JOYAXISMOTION or
            event.type == pygame.JOYHATMOTION or
            event.type == pygame.JOYBUTTONDOWN) and game_over:
            running = False
        if event.type == pygame.JOYAXISMOTION:
            selected_cell[event.axis % 2] += int(event.value)
            if check_selected_cell():
                if level[selected_cell[1]][selected_cell[0]] == "x":
                    selected_cell[event.axis % 2] -= int(event.value)
        if event.type == pygame.JOYHATMOTION:
            if joysticks[0].get_hat(0)[0] != 0 and joysticks[0].get_hat(0)[1] != 0:
                continue
            selected_cell[0] += joysticks[0].get_hat(0)[0]
            selected_cell[1] -= joysticks[0].get_hat(0)[1]
            if check_selected_cell():
                if level[selected_cell[1]][selected_cell[0]] == "x":
                    selected_cell[0] -= joysticks[0].get_hat(0)[0]
                    selected_cell[1] += joysticks[0].get_hat(0)[1]
        if event.type == pygame.KEYDOWN and (event.key == 100 or event.key == 1073741903):
            # d
            selected_cell[0] += 1
            if check_selected_cell():
                if level[selected_cell[1]][selected_cell[0]] == "x":
                    selected_cell[0] -= 1
        if event.type == pygame.KEYDOWN and (event.key == 97 or event.key == 1073741904):
            # a
            selected_cell[0] -= 1
            if check_selected_cell():
                if level[selected_cell[1]][selected_cell[0]] == "x":
                    selected_cell[0] += 1
        if event.type == pygame.KEYDOWN and (event.key == 115 or event.key == 1073741905):
            # s
            selected_cell[1] += 1
            if check_selected_cell():
                if level[selected_cell[1]][selected_cell[0]] == "x":
                    selected_cell[1] -= 1
        if event.type == pygame.KEYDOWN and (event.key == 119 or event.key == 1073741906):
            # w
            selected_cell[1] -= 1
            if check_selected_cell():
                if level[selected_cell[1]][selected_cell[0]] == "x":
                    selected_cell[1] += 1

        if not selecting_kill and not selecting_tree and not moving_tree and not game_over and\
                ((event.type == pygame.JOYBUTTONDOWN and event.button == 1) or
                 (event.type == pygame.KEYDOWN and event.key in [13, 32]) or
                 (event.type == pygame.MOUSEBUTTONDOWN and board.get_cell(event.pos) is not None and
                  list(board.get_cell(event.pos)) == selected_cell)):
            # Выбор/ход фигуры
            if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and\
                    board.boardpiece[selected_cell[1]][selected_cell[0]].color == board.playerslive[board.hod]:
                chosen_cell = selected_cell[::]
                move_cells, kill_cells = board.moved_cells()
            elif selected_cell in move_cells or selected_cell in kill_cells:
                board.move_piece()
                if board.boardpiece[selected_cell[1]][selected_cell[0]].tree:
                    board.boardpiece[selected_cell[1]][selected_cell[0]].tree = False
                    board.boardpiece[selected_cell[1]][selected_cell[0]].move()

        if selecting_tree and\
                ((event.type == pygame.JOYBUTTONDOWN and event.button == 1) or
                 (event.type == pygame.KEYDOWN and event.key in [13, 32]) or
                 (event.type == pygame.MOUSEBUTTONDOWN and board.get_cell(event.pos) is not None and
                  list(board.get_cell(event.pos)) == selected_cell)):
            # Выбор дерева
            if level[selected_cell[1]][selected_cell[0]] == '#':
                level[selected_cell[1]][selected_cell[0]] = '.'
                for sprite in other_sprites:
                    if sprite.x == selected_cell[0] and sprite.y == selected_cell[1]:
                        sprite.x = 500
                        sprite.y = 500
                        sprite.move()
                        break
                if not board.boardpiece[selected_cell[1]][selected_cell[0]] is None:
                    board.boardpiece[selected_cell[1]][selected_cell[0]].tree = False
                    board.boardpiece[selected_cell[1]][selected_cell[0]].move()
                selecting_tree = False
                moving_tree = True
                if not (selectinging_image is None):
                    selectinging_image.kill()
                continue

        if moving_tree and\
                ((event.type == pygame.JOYBUTTONDOWN and event.button == 1) or
                 (event.type == pygame.KEYDOWN and event.key in [13, 32]) or
                 (event.type == pygame.MOUSEBUTTONDOWN and board.get_cell(event.pos) is not None and
                  list(board.get_cell(event.pos)) == selected_cell)):
            # Передвижение дерева
            if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and\
                    board.boardpiece[selected_cell[1]][selected_cell[0]].color == board.playerslive[board.hod] and\
                    level[selected_cell[1]][selected_cell[0]] != '@':
                board.boardpiece[selected_cell[1]][selected_cell[0]].tree = True
                board.boardpiece[selected_cell[1]][selected_cell[0]].move()
                level[selected_cell[1]][selected_cell[0]] = '#'
                for sprite in other_sprites:
                    if sprite.x == 500 and sprite.y == 500:
                        sprite.x = selected_cell[0]
                        sprite.y = selected_cell[1]
                        sprite.move()
                        break
                moving_tree = False
                selecting_kill = True
                if not (selectinging_image is None):
                    selectinging_image.kill()

        if selecting_kill and\
                ((event.type == pygame.JOYBUTTONDOWN and event.button == 1) or
                 (event.type == pygame.KEYDOWN and event.key in [13, 32]) or
                 (event.type == pygame.MOUSEBUTTONDOWN and board.get_cell(event.pos) is not None and
                  list(board.get_cell(event.pos)) == selected_cell)):
            # Выбор убийства фигуры
            if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and\
                    board.boardpiece[selected_cell[1]][selected_cell[0]].color != board.playerslive[board.hod] and\
                    not (type(board.boardpiece[selected_cell[1]][selected_cell[0]]) is King):
                board.kill(selected_cell)
                selecting_kill = False
                board.hod = (board.hod + 1) % len(board.playerslive)
                if not (selectinging_image is None):
                    selectinging_image.kill()

        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont("Bauhaus 93", 30)
    if game_over:
        text = "Player " + str(board.playerslive[board.hod]) + " win"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 90))
        text = "Press any key to continue"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 50))
    elif selecting_tree:
        text = "Player " + str(board.playerslive[board.hod])
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 90))
        text = "Select tree to move"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 50))
        if level[selected_cell[1]][selected_cell[0]] == '#':
            if not (selectinging_image is None):
                selectinging_image.kill()
            selectinging_image = SelectImage(selected_cell[0], selected_cell[1])
        elif not (selectinging_image is None):
            selectinging_image.kill()
    elif moving_tree:
        text = "Player " + str(board.playerslive[board.hod])
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 90))
        text = "Select piece to place on tree"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 50))
        if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and\
                board.boardpiece[selected_cell[1]][selected_cell[0]].color == board.playerslive[board.hod] and\
                level[selected_cell[1]][selected_cell[0]] != '@':
            if not (selectinging_image is None):
                selectinging_image.kill()
            selectinging_image = SelectImage(selected_cell[0], selected_cell[1])
        elif not (selectinging_image is None):
            selectinging_image.kill()
    elif selecting_kill:
        text = "Player " + str(board.playerslive[board.hod])
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 90))
        text = "Select piece to kill"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 50))
        if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and\
                board.boardpiece[selected_cell[1]][selected_cell[0]].color != board.playerslive[board.hod] and \
                not (type(board.boardpiece[selected_cell[1]][selected_cell[0]]) is King):
            if not (selectinging_image is None):
                selectinging_image.kill()
            selectinging_image = SelectImage(selected_cell[0], selected_cell[1])
        elif not (selectinging_image is None):
            selectinging_image.kill()
    else:
        text = "Player " + str(board.playerslive[board.hod]) + " move"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 50))
    tile_sprites.draw(screen)
    other_sprites.draw(screen)
    piece_sprites.draw(screen)
    board.render()
    pygame.display.flip()
    clock.tick(FPS)
terminate()
