import pygame
import sys
import os

all_sprites = pygame.sprite.Group()
tile_sprites = pygame.sprite.Group()
piece_sprites = pygame.sprite.Group()
tree_sprites = pygame.sprite.Group()
particles_sprites = pygame.sprite.Group()

red_piece_sprites = pygame.sprite.Group()
blue_piece_sprites = pygame.sprite.Group()
black_piece_sprites = pygame.sprite.Group()

FPS = 60
clock = pygame.time.Clock()
tile_width = tile_height = 50
size = width, height = tile_width * 9 + 50, tile_height * 9 + 150

screen_rect = (0, 0, width, height)
screen = pygame.display.set_mode(size)


def terminate():
    """Выход из приложения"""
    pygame.quit()
    pygame.mixer.quit()
    pygame.font.quit()
    pygame.joystick.quit()
    sys.exit()


def load_image(name, colorkey=None):
    """Загрузка изображения из папки data"""
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

    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map)), maximum
