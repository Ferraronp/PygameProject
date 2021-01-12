import sys
import os
from pprint import pprint
from random import randrange
import random
import pygame

from values import *
from menu import start

COLORS = ["red", "blue", "black"]
left = 25
top = 25
gold_block = (0, 0)

pygame.init()
pygame.font.init()
pygame.joystick.init()
pygame.mixer.init()


code = "IDDQD"
i = 0


class Board:
    def __init__(self, players, left, top, maximum):
        """Поле с фигурами
        players - количество игроков от 2 до 3"""
        self.boardpiece = [[]]
        self.players = ["red", "blue", "black"][:players]
        self.playerslive = self.players[::]
        self.hod = randrange(0, players)
        self.kolvo = players
        self.left = left
        self.top = top
        self.maximum = maximum
        self.cell_size = tile_width

    def render(self, kill_cells, move_cells, selected_cell, chosen_cell):
        """Отрисовка краёв поля, клеток передвижения и сруба, выбранных клеток"""
        pygame.draw.rect(screen, "black", (self.left,
                                           self.top,
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

    def get_click(self, pos):
        cell = self.get_cell(pos)
        global selected_cell
        if cell is not None and not level[cell[1]][cell[0]] == 'x':
            selected_cell = list(cell)

    def get_cell(self, pos):
        """Определение клетки по которой кликнули"""
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if -1 < x < len(self.boardpiece) and -1 < y < len(self.boardpiece[0]):
            return x, y
        return None

    def moved_cells(self, chosen_cell, level, selecting_kill=False):
        """Отправка сигнала для передвижения фигуры"""
        return self.boardpiece[chosen_cell[1]][chosen_cell[0]].can_move(chosen_cell,
                                                                        self,
                                                                        level,
                                                                        selecting_kill,
                                                                        self.maximum)

    def move_piece(self, chosen_cell, selected_cell, move_cells, kill_cells):
        """Передвижение фигуры"""
        global game_over, selecting_tree, was_on_gold
        self.kill(selected_cell, chosen_cell)

        try:
            if selected_cell[1] == gold_block[1] and selected_cell[0] == gold_block[0] and\
                    (not was_on_gold[self.boardpiece[chosen_cell[1]][chosen_cell[0]].color] or
                            type(self.boardpiece[chosen_cell[1]][chosen_cell[0]]) is King):
                if type(self.boardpiece[chosen_cell[1]][chosen_cell[0]]) is King:
                    game_over = True
                    self.playerslive = [self.boardpiece[chosen_cell[1]][chosen_cell[0]].color]
                else:
                    was_on_gold[self.boardpiece[chosen_cell[1]][chosen_cell[0]].color] = True
                    selecting_tree = True
        except Exception:
            pass

        self.boardpiece[chosen_cell[1]][chosen_cell[0]].x = selected_cell[0]
        self.boardpiece[chosen_cell[1]][chosen_cell[0]].y = selected_cell[1]
        self.boardpiece[selected_cell[1]][selected_cell[0]] = self.boardpiece[chosen_cell[1]][chosen_cell[0]]
        self.boardpiece[chosen_cell[1]][chosen_cell[0]].move()
        self.boardpiece[chosen_cell[1]][chosen_cell[0]] = None
        try:
            if not selecting_tree:
                self.hod = (self.hod + 1) % len(self.playerslive)
            if len(self.playerslive) == 1:
                game_over = True
            if game_over:
                fonmusic.stop()
                pygame.mixer.Sound('data\\win.mp3').play()
                clock.tick(2000)
        except Exception:
            pass

    def kill(self, cell, chosen_cell):
        """Срубание фигуры"""
        if self.boardpiece[cell[1]][cell[0]] is None:
            return
        if type(self.boardpiece[cell[1]][cell[0]]) is King:
            if self.boardpiece[cell[1]][cell[0]].color == "red":
                del self.playerslive[self.playerslive.index("red")]
                for sprite in red_piece_sprites:
                    self.boardpiece[sprite.y][sprite.x] = None
                    try:
                        level[sprite.y][sprite.x] = '.'
                    except Exception:
                        pass
                    sprite.kill()
            elif self.boardpiece[cell[1]][cell[0]].color == "blue":
                del self.playerslive[self.playerslive.index("blue")]
                for sprite in blue_piece_sprites:
                    self.boardpiece[sprite.y][sprite.x] = None
                    try:
                        level[sprite.y][sprite.x] = '.'
                    except Exception:
                        pass
                    sprite.kill()
            elif self.boardpiece[cell[1]][cell[0]].color == "black":
                del self.playerslive[self.playerslive.index("black")]
                for sprite in black_piece_sprites:
                    self.boardpiece[sprite.y][sprite.x] = None
                    try:
                        level[sprite.y][sprite.x] = '.'
                    except Exception:
                        pass
                    sprite.kill()
            self.hod = self.playerslive.index(self.boardpiece[chosen_cell[1]][chosen_cell[0]].color)
        else:
            self.boardpiece[cell[1]][cell[0]].kill()
            self.boardpiece[cell[1]][cell[0]] = None
        pygame.mixer.Sound('data\\kill.mp3').play()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y, left, top):
        """Спрайт части поля"""
        super().__init__(all_sprites, tile_sprites)
        global tile_images
        self.x = x
        self.y = y
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * x + left, tile_height * y + top)


class Piece(pygame.sprite.Sprite):
    def __init__(self, color, x, y, left, top, tree=False):
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
        self.left = left
        self.top = top
        imagename = type(self).__name__.lower() + "_" + self.color + ".png"
        self.image = load_image(imagename)
        self.rect = self.image.get_rect().move(
            tile_width * self.x + self.left, tile_height * self.y + self.top)

    def can_move_like_rook(self, chosen_cell, board, level, selecting_kill, maximum):
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

    def can_move_like_bishop(self, chosen_cell, board, level, selecting_kill, maximum):
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
        """Передвижение спрайта"""
        self.rect = self.image.get_rect().move(
            tile_width * self.x + self.left, tile_height * self.y + self.top - (self.tree * 19))


class King(Piece):
    def can_move(self, chosen_cell, board, level, selecting_kill, maximum):
        move_cells1, kill_cells1 = self.can_move_like_bishop(chosen_cell,
                                                             board, level, selecting_kill, maximum)
        move_cells2, kill_cells2 = self.can_move_like_rook(chosen_cell,
                                                           board, level, selecting_kill, maximum)
        return move_cells1 + move_cells2, kill_cells1 + kill_cells2


class Rook(Piece):
    def can_move(self, chosen_cell, board, level, selecting_kill, maximum):
        move_cells, kill_cells = self.can_move_like_rook(chosen_cell, board,
                                                         level, selecting_kill, maximum)
        return move_cells, kill_cells


class Bishop(Piece):
    def can_move(self, chosen_cell, board, level, selecting_kill, maximum):
        move_cells, kill_cells = self.can_move_like_bishop(chosen_cell, board,
                                                           level, selecting_kill, maximum)
        return move_cells, kill_cells


class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, left, top):
        """Спрайт дерева"""
        super().__init__(all_sprites, tree_sprites)
        self.x = x
        self.y = y
        self.left = left
        self.top = top
        self.image = load_image("tree.png")
        self.rect = self.image.get_rect().move(
            tile_width * self.x + self.left, tile_height * self.y + self.top)

    def move(self):
        """Передвижение спрайта после хода на золотую клетку"""
        self.rect = self.image.get_rect().move(
            tile_width * self.x + self.left, tile_height * self.y + self.top)


class SelectImage(pygame.sprite.Sprite):
    def __init__(self, x, y, left, top):
        """Спрайт выбора клетки дерева, срубания клетки"""
        super().__init__(all_sprites, piece_sprites)
        self.x = x
        self.y = y
        self.image = load_image("chosing.png")
        self.rect = self.image.get_rect().move(
            tile_width * self.x + left, tile_height * self.y + top)


def generate_level(level, board, left, top):
    """Создание спрайтов в начале игры"""
    i = 1
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in ['6', '7', '8'] and board.kolvo == 2:
                level[y][x] = '.'
            if level[y][x] == 'x':
                board.boardpiece[y] += [None]
                Tile("none", x, y, left, top)
            elif level[y][x] == '@':
                Tile("gold", x, y, left, top)
                global gold_block
                gold_block = (x, y)
                board.boardpiece[y] += [None]
            elif level[y][x] == '.':
                board.boardpiece[y] += [None]
                Tile("empty" + str(i % 2 + 1), x, y, left, top)
            elif level[y][x] == '#':
                board.boardpiece[y] += [None]
                Tile("empty" + str(i % 2 + 1), x, y, left, top)
                Tree(x, y, left, top)
            elif int(level[y][x]) % 3 == 0:
                Tile("empty" + str(i % 2 + 1), x, y, left, top)
                board.boardpiece[y] += [King(COLORS[(int(level[y][x])) // 3], x, y, left, top)]
                level[y][x] = '.'
            elif int(level[y][x]) % 3 == 1:
                Tile("empty" + str(i % 2 + 1), x, y, left, top)
                board.boardpiece[y] += [Rook(COLORS[(int(level[y][x])) // 3], x, y, left, top)]
                level[y][x] = '.'
            elif int(level[y][x]) % 3 == 2:
                Tile("empty" + str(i % 2 + 1), x, y, left, top)
                board.boardpiece[y] += [Bishop(COLORS[(int(level[y][x])) // 3], x, y, left, top)]
                level[y][x] = '.'
            i += 1
        board.boardpiece += [[]]
    del board.boardpiece[-1]


def check_selected_cell():
    """Проверка выбранной клетки на нахождение внутри поля"""
    res = True
    for i in range(2):
        if selected_cell[i] < 0:
            selected_cell[i] = 0
            res = False
        elif selected_cell[i] >= maximum[i]:
            selected_cell[i] = maximum[i]
            res = False
    return res


class Particle(pygame.sprite.Sprite):
    fire = [load_image("particle.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        """Создание анимированного спрайта"""
        super().__init__(particles_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.i = 0

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 5

    def update(self):
        self.i += 1
        if self.i == 2:
            self.i = 0
            self.velocity[1] += self.gravity
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            if not self.rect.colliderect(screen_rect):
                self.kill()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        """Создание светошумовой"""
        super().__init__(particles_sprites)
        self.i = 0
        self.ux = 20
        self.uy = 1
        self.updating = False
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        pygame.mixer.Sound('data\\flashbang_hit.mp3').play()

    def cut_sheet(self, sheet, columns, rows):
        """Разделение картинки для анимирования"""
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(pygame.transform.flip(pygame.transform.rotate(
                    sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)), 270), True, False), (100, 60)))

    def update(self):
        """Обновление картинки спрайта"""
        if not self.updating:
            return
        self.i += 1
        if self.i != 3:
            return
        self.i = 0
        self.cur_frame = self.cur_frame + 1
        if len(self.frames) == self.cur_frame:
            pygame.mixer.Sound('data\\flashbang_explode.mp3').play()
            create_particles(self.rect[:2])
        if len(self.frames) <= self.cur_frame:
            return
        self.image = self.frames[self.cur_frame]

    def move(self):
        """Передвижение спрайта"""
        if self.updating:
            return
        self.i += 1
        for sprite in tile_sprites:
            if pygame.sprite.collide_mask(self, sprite) and level[sprite.y][sprite.x] == '.':
                pygame.mixer.Sound('data\\flashbang_hit.mp3').play()
                self.ux = self.ux // 2
                self.uy = -int(self.uy) // 1.5 - 2
                if self.uy >= 0:
                    self.updating = True
                    self.i = 0
                    return
        self.uy += 1 * self.i // 5
        self.rect = self.rect.move(self.ux, self.uy)


def create_particles(position):
    """Создание частиц"""
    particle_count = 1000
    numbers = range(-100, 100)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def drawing():
    """Отрисовка экрана"""
    global selectinging_image
    screen.blit(fon, (0, 0))
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
            selectinging_image = SelectImage(selected_cell[0], selected_cell[1], left, top)
        elif not (selectinging_image is None):
            selectinging_image.kill()
    elif moving_tree:
        text = "Player " + str(board.playerslive[board.hod])
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 90))
        text = "Select piece to place on tree"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 50))
        if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and \
                board.boardpiece[selected_cell[1]][selected_cell[0]].color == board.playerslive[board.hod] and \
                level[selected_cell[1]][selected_cell[0]] != '@':
            if not (selectinging_image is None):
                selectinging_image.kill()
            selectinging_image = SelectImage(selected_cell[0], selected_cell[1], left, top)
        elif not (selectinging_image is None):
            selectinging_image.kill()
    elif selecting_kill:
        text = "Player " + str(board.playerslive[board.hod])
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 90))
        text = "Select piece to kill"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 50))
        if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and \
                board.boardpiece[selected_cell[1]][selected_cell[0]].color != board.playerslive[board.hod] and \
                not (type(board.boardpiece[selected_cell[1]][selected_cell[0]]) is King):
            if not (selectinging_image is None):
                selectinging_image.kill()
            selectinging_image = SelectImage(selected_cell[0], selected_cell[1], left, top)
        elif not (selectinging_image is None):
            selectinging_image.kill()
    else:
        text = "Player " + str(board.playerslive[board.hod]) + " move"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 50))
    tile_sprites.draw(screen)
    tree_sprites.draw(screen)
    particles_sprites.draw(screen)
    particles_sprites.update()
    piece_sprites.draw(screen)
    board.render(kill_cells, move_cells, selected_cell, chosen_cell)


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

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

playerskolvo = start(Board, SelectImage, generate_level)

level, maximum = load_level("map" + str(playerskolvo) + "_" + str(randrange(1, 6)) + ".txt")
selected_cell = (4, 4)
board = Board(playerskolvo, left, top, maximum)
generate_level(level, board, left, top)

SLEEPEVENT = pygame.USEREVENT + 1
sleeptime = 1000 * 60
pygame.time.set_timer(SLEEPEVENT, sleeptime)
sleepevent_was = False
f = False

fon = pygame.transform.scale(load_image('fon.png'), (width, height))

lines = open("settings.txt", encoding="utf8", mode="r").readlines()
try:
    volume = 100
    for line in lines:
        if "volume=" == line[:7]:
            volume = int(line[7:])
            if not (0 <= volume <= 100):
                volume = 100
            break
except Exception:
    volume = 100
fonmusic = pygame.mixer.Sound('data\\fon.mp3')
fonmusic.set_volume(volume / 100)
fonmusic.play(600)

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

    events = pygame.event.get()
    if events and not sleepevent_was:
        pygame.time.set_timer(SLEEPEVENT, sleeptime)
    if len(particles_sprites) == 1 and f:
        for flashbang in particles_sprites:
            flashbang.kill()
            fonmusic.play(600)
    elif len(particles_sprites) == 1 and not f:
        for flashbang in particles_sprites:
            flashbang.move()
    elif len(particles_sprites) > 1:
        f = True

    for event in events:
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
                    board.boardpiece[selected_cell[1]][selected_cell[0]].color ==\
                    board.playerslive[board.hod]:
                chosen_cell = selected_cell[::]
                move_cells, kill_cells = board.moved_cells(chosen_cell, level, selecting_kill)
            elif selected_cell in move_cells or selected_cell in kill_cells:
                board.move_piece(chosen_cell, selected_cell, move_cells, kill_cells)
                chosen_cell = False
                move_cells = []
                kill_cells = []
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
                for sprite in tree_sprites:
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
                pygame.mixer.Sound('data\\tree.mp3').play()
                continue

        if moving_tree and\
                ((event.type == pygame.JOYBUTTONDOWN and event.button == 1) or
                 (event.type == pygame.KEYDOWN and event.key in [13, 32]) or
                 (event.type == pygame.MOUSEBUTTONDOWN and board.get_cell(event.pos) is not None and
                  list(board.get_cell(event.pos)) == selected_cell)):
            # Передвижение дерева
            if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and\
                    board.boardpiece[selected_cell[1]][selected_cell[0]].color ==\
                    board.playerslive[board.hod] and\
                    level[selected_cell[1]][selected_cell[0]] != '@':
                board.boardpiece[selected_cell[1]][selected_cell[0]].tree = True
                board.boardpiece[selected_cell[1]][selected_cell[0]].move()
                level[selected_cell[1]][selected_cell[0]] = '#'
                for sprite in tree_sprites:
                    if sprite.x == 500 and sprite.y == 500:
                        sprite.x = selected_cell[0]
                        sprite.y = selected_cell[1]
                        sprite.move()
                        break
                moving_tree = False
                selecting_kill = True
                if not (selectinging_image is None):
                    selectinging_image.kill()
                pygame.mixer.Sound('data\\tree.mp3').play()

        if selecting_kill and\
                ((event.type == pygame.JOYBUTTONDOWN and event.button == 1) or
                 (event.type == pygame.KEYDOWN and event.key in [13, 32]) or
                 (event.type == pygame.MOUSEBUTTONDOWN and board.get_cell(event.pos) is not None and
                  list(board.get_cell(event.pos)) == selected_cell)):
            # Выбор убийства фигуры
            if not (board.boardpiece[selected_cell[1]][selected_cell[0]] is None) and\
                    board.boardpiece[selected_cell[1]][selected_cell[0]].color !=\
                    board.playerslive[board.hod] and\
                    not (type(board.boardpiece[selected_cell[1]][selected_cell[0]]) is King):
                board.kill(selected_cell, selected_cell)
                selecting_kill = False
                board.hod = (board.hod + 1) % len(board.playerslive)
                if not (selectinging_image is None):
                    selectinging_image.kill()

        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)

        if event.type == SLEEPEVENT and not sleepevent_was and pygame.mouse.get_focused():
            fonmusic.stop()
            sleepevent_was = True
            image = load_image("flashbang.png")
            AnimatedSprite(image, 4, 2, -200, 0)
    drawing()
    pygame.display.flip()
    clock.tick(FPS)
terminate()
