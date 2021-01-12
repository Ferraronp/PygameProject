import sys
import os
from pprint import pprint
from random import randrange
import random
import pygame
from values import *


def generate():
    global board, level, selected_cell, maximum
    level, maximum = load_level(f"training\\map{window_num}.txt")
    board = Board(3, left, top, [5, 5])
    board.hod = 0
    generate_level(level, board, left, top)

    if window_num == 10:
        for sprite in piece_sprites:
            if sprite.x == 1 and sprite.y == 1:
                sprite.x = 2
                sprite.y = 2
                sprite.tree = True
                board.boardpiece[2][2] = board.boardpiece[1][1]
                board.boardpiece[1][1] = None
                sprite.move()


def delete():
    for sprite in all_sprites:
        sprite.kill()


def drawing(rects, texts, mousex, mousey):
    global move_cells, kill_cells, window_num, itr
    screen.blit(fon, (0, 0))

    for i in range(len(rects)):
        if window_num == 1 and i == 0:
            continue
        '''if window_num != windows_count and i == 2:
            continue'''
        if window_num == windows_count and i == 1:
            continue
        if rects[i][0].left <= mousex <= rects[i][0].left + rects[i][0].width and \
                rects[i][0].top <= mousey <= rects[i][0].top + rects[i][0].height:
            color = "red"
        else:
            color = "blue"
        pygame.draw.rect(screen, "white",
                         (rects[i][0].left - 1, rects[i][0].top - 1,
                          rects[i][0].width + 2, rects[i][0].height + 2))
        pygame.draw.rect(screen, color, (rects[i][0].left, rects[i][0].top,
                                         rects[i][0].width, rects[i][0].height))
        screen.blit(*texts[i])

    all_sprites.draw(screen)
    tile_sprites.draw(screen)
    tree_sprites.draw(screen)
    piece_sprites.draw(screen)
    board.render(kill_cells, move_cells, selected_cell, chosen_cell)
    if window_num == 2 and 80 < itr:
        font = pygame.font.SysFont("Bauhaus 93", 30)
        text = "Player " + str(board.playerslive[board.hod]) + " win"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 110))
    if window_num == 9:
        font = pygame.font.SysFont("Bauhaus 93", 30)
        text = "Player " + str(board.playerslive[board.hod]) + " move"
        text = font.render(text, False, board.playerslive[board.hod])
        screen.blit(text, (10, height - 110))


def moving():
    global window_num, itr, chosen_cell, move_cells, kill_cells, level, music, g
    itr += 1
    if window_num == 1:
        if itr == 40:
            chosen_cell = [1, 1]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 80:
            board.move_piece(chosen_cell, [2, 1], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 120:
            chosen_cell = [3, 3]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 160:
            board.move_piece(chosen_cell, [3, 2], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 200:
            chosen_cell = [2, 1]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 240:
            board.move_piece(chosen_cell, [3, 1], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 280:
            chosen_cell = [3, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 320:
            board.move_piece(chosen_cell, [2, 2], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 360:
            chosen_cell = [3, 1]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 400:
            board.move_piece(chosen_cell, [2, 1], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 440:
            chosen_cell = [2, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 480:
            board.move_piece(chosen_cell, [3, 3], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 560:
            chosen_cell = [2, 1]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 600:
            board.move_piece(chosen_cell, [1, 1], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 640:
            itr = 0
    elif window_num == 2:
        if itr == 40:
            chosen_cell = [1, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 80:
            board.move_piece(chosen_cell, [2, 2], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
            if music:
                pygame.mixer.Sound('data\\win.mp3').play()
            music = False
        elif itr == 120:
            board.move_piece([2, 2], [1, 2], move_cells, kill_cells)
            itr = 1
    elif window_num == 3:
        if itr == 40:
            chosen_cell = [1, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 80:
            board.move_piece(chosen_cell, [2, 2], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 120:
            board.move_piece([2, 2], [1, 2], move_cells, kill_cells)
            delete()
            generate()
            itr = 0
    elif window_num == 4:
        if itr == 40:
            chosen_cell = [2, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 80:
            board.move_piece(chosen_cell, [2, 1], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 120:
            chosen_cell = [2, 1]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 160:
            board.move_piece(chosen_cell, [2, 2], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 200:
            itr = 0
    elif window_num == 5:
        if itr == 40:
            chosen_cell = [2, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 80:
            board.move_piece(chosen_cell, [1, 1], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 120:
            chosen_cell = [1, 1]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 160:
            board.move_piece(chosen_cell, [2, 2], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 200:
            itr = 0
    elif window_num == 6:
        if itr == 40:
            chosen_cell = [2, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 80:
            board.move_piece(chosen_cell, [1, 1], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 120:
            chosen_cell = [1, 1]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 160:
            board.move_piece(chosen_cell, [2, 1], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 200:
            chosen_cell = [2, 1]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 240:
            board.move_piece(chosen_cell, [2, 2], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 280:
            itr = 0
    elif window_num == 7:
        if itr == 40:
            chosen_cell = [2, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 80:
            board.move_piece(chosen_cell, [2, 3], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 120:
            chosen_cell = [2, 3]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 160:
            board.move_piece(chosen_cell, [2, 2], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 200:
            itr = 0
    elif window_num == 8:
        if itr == 40:
            chosen_cell = [1, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 80:
            board.move_piece(chosen_cell, [2, 2], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 120:
            delete()
            generate()
            itr = 0
    elif window_num == 9:
        if itr == 40:
            chosen_cell = [2, 3]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 80:
            board.move_piece(chosen_cell, [2, 2], move_cells, kill_cells)
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 120:
            g = SelectImage(1, 2, left, top)
        elif itr == 160:
            g.kill()
        elif itr == 200:
            global tree_sprites
            for tree in tree_sprites:
                tree.x = -500
                tree.y = -500
                tree.move()
        elif itr == 240:
            g = SelectImage(1, 3, left, top)
        elif itr == 280:
            g.kill()
            for tree in tree_sprites:
                tree.x = 1
                tree.y = 3
                tree.move()
            for sprite in piece_sprites:
                if sprite.x == 1 and sprite.y == 3:
                    sprite.tree = True
                    sprite.move()
                    break
        elif itr == 320:
            g = SelectImage(3, 1, left, top)
        elif itr == 360:
            g.kill()
        elif itr == 400:
            board.boardpiece[1][3].kill()
            board.hod = 1
        elif itr == 440:
            delete()
            generate()
            itr = 0
    elif window_num == 10:
        if itr == 40:
            chosen_cell = [1, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 80:
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 120:
            chosen_cell = [2, 2]
            move_cells, kill_cells = board.moved_cells(chosen_cell, level)
        elif itr == 160:
            board.move_piece(chosen_cell, [1, 2], move_cells, kill_cells)
            board.boardpiece[2][1].tree = False
            board.boardpiece[2][1].move()
            chosen_cell = False
            move_cells = []
            kill_cells = []
        elif itr == 200:
            delete()
            generate()
            itr = 0


def training():
    intro_text = [("Назад", "-"),
                  ("Далее", "+"),
                  ("Закрыть", start_screen)]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 25
    rects = []
    texts = []
    global window_num, windows_count, itr, move_cells, kill_cells, chosen_cell, music
    move_cells = []
    kill_cells = []
    itr = 0
    window_num = 1
    windows_count = 10
    generate()
    for line, cmd in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        intro_rect.left = text_coord + 10
        intro_rect.y = 550
        rects += [(pygame.draw.rect(screen, "blue", (text_coord - 10, intro_rect.y - 15, 150, 50), width=0), cmd)]
        text_coord += intro_rect.width
        screen.blit(string_rendered, intro_rect)
        texts += [(string_rendered, intro_rect)]
        text_coord += 100
    mousex, mousey = 0, 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, f in enumerate(rects):
                    if i == 0 and window_num == 1:
                        continue
                    if i == 1 and window_num == windows_count:
                        continue
                    '''if i == 2 and window_num != windows_count:
                        continue'''
                    rect, cmd = f
                    if rect.left <= event.pos[0] <= rect.left + rect.width and \
                            rect.top <= event.pos[1] <= rect.top + rect.height:
                        itr = 0
                        chosen_cell = False
                        move_cells = []
                        kill_cells = []
                        music = True
                        if cmd == "+":
                            window_num += 1
                            delete()
                            generate()
                            continue
                        elif cmd == "-":
                            window_num -= 1
                            delete()
                            generate()
                            continue
                        delete()
                        return cmd()
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
        drawing(rects, texts, mousex, mousey)
        pygame.display.flip()
        clock.tick(FPS)
        moving()


def settings():
    global volume
    buttons = [("Назад", start_screen)]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 25
    rects = []
    texts = []
    for line, cmd in buttons:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        intro_rect.left = text_coord + 10
        intro_rect.y = 550
        rects += [(pygame.draw.rect(screen, "blue", (text_coord - 10, intro_rect.y - 15, 150, 50), width=0), cmd)]
        text_coord += intro_rect.width
        text_coord += 250
        screen.blit(string_rendered, intro_rect)
        texts += [(string_rendered, intro_rect)]
    mousex, mousey = 0, 0

    fonmusic = pygame.mixer.Sound('data\\fon.mp3')
    fonmusic.set_volume(volume / 100)
    fonmusic.play(500)

    x, y = 20 + volume / 100 * 440, 50
    deltax = 0
    drawing = False
    textvolume = font.render("Volume ", 1, pygame.Color('yellow'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, cmd in rects:
                    if rect.left <= event.pos[0] <= rect.left + rect.width and \
                            rect.top <= event.pos[1] <= rect.top + rect.height:
                        if cmd == "exit":
                            fonmusic.stop()
                            return
                        fonmusic.stop()
                        return cmd()

                if x <= event.pos[0] <= x + 100 and \
                        y <= event.pos[1] <= y + 100:
                    drawing = True
                    deltax = event.pos[0] - x
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
                if drawing:
                    if event.pos[0] - deltax < 20:
                        volume = 0
                        x = 20
                    elif 460 < event.pos[0] - deltax:
                        volume = 100
                        x = 460
                    else:
                        x = event.pos[0] - deltax
                        volume = int(x / 460 * 100)
                        fonmusic.set_volume(volume / 100)
        fon = pygame.transform.scale(load_image('fon.png'), (width, height))
        screen.blit(fon, (0, 0))
        for i in range(len(rects)):
            if rects[i][0].left <= mousex <= rects[i][0].left + rects[i][0].width and \
                    rects[i][0].top <= mousey <= rects[i][0].top + rects[i][0].height:
                color = "red"
            else:
                color = "blue"
            pygame.draw.rect(screen, "white",
                             (rects[i][0].left - 1, rects[i][0].top - 1, rects[i][0].width + 2, rects[i][0].height + 2))
            pygame.draw.rect(screen, color, (rects[i][0].left, rects[i][0].top, rects[i][0].width, rects[i][0].height))
            screen.blit(*texts[i])
        pygame.draw.rect(screen, "white",
                         (19, 49, 462, 102), width=1)
        pygame.draw.rect(screen, "blue",
                         (x, y, 20, 100))
        rect = textvolume.get_rect()
        rect.x += 20
        rect.y += 20
        screen.blit(textvolume, rect)
        text = font.render(str(volume) + " %", 1, pygame.Color('yellow'))
        rect.x += rect.width
        screen.blit(text, rect)
        pygame.display.flip()
        clock.tick(FPS)


def select_count_of_players():
    buttons = [("2 игрока", "exit"),
               ("3 игрока", "exit"),
               ("Назад", start_screen)]

    screen.blit(fon, (0, 0))
    screen.blit(fonplus, (100, 10))

    font = pygame.font.Font(None, 30)
    text_coord = 160
    rects = []
    texts = []
    for line, cmd in buttons:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 50
        rects += [(pygame.draw.rect(screen, "blue", (intro_rect.x - 15, text_coord - 15, 150, 50),
                                    width=0), cmd)]
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        texts += [(string_rendered, intro_rect)]
    mousex, mousey = 0, 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, f in enumerate(rects):
                    rect, cmd = f
                    if rect.left <= event.pos[0] <= rect.left + rect.width and \
                            rect.top <= event.pos[1] <= rect.top + rect.height:
                        if cmd == "exit":
                            return i + 2
                        return cmd()
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
        for i, f in enumerate(rects):
            rect, cmd = f
            if rect.left <= mousex <= rect.left + rect.width and \
                    rect.top <= mousey <= rect.top + rect.height:
                color = "red"
            else:
                color = "blue"
            pygame.draw.rect(screen, "white",
                             (rect.left - 1, rect.top - 1, rect.width + 2, rect.height + 2))
            pygame.draw.rect(screen, color, (rect.left, rect.top, rect.width, rect.height))
            screen.blit(*texts[i])
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    f = open("settings.txt", mode="w")
    f.write("volume=" + str(volume))
    f.close()
    egg = [4, 4, 6, 6, 7, 5, 7, 5, 13, 14, 3]
    buttons = [("Начать игру", select_count_of_players),
               ("Обучение", training),
               ("Настройки", settings)]

    screen.blit(fon, (0, 0))
    screen.blit(fonplus, (100, 10))
    font = pygame.font.Font(None, 30)
    text_coord = 160
    rects = []
    texts = []
    for line, cmd in buttons:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 50
        rects += [(pygame.draw.rect(screen, "blue",
                                    (intro_rect.x - 15, text_coord - 15, 150, 50), width=0), cmd)]
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
                    if rect.left <= event.pos[0] <= rect.left + rect.width and \
                            rect.top <= event.pos[1] <= rect.top + rect.height:
                        if cmd == "exit":
                            return
                        return cmd()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == egg[f]:
                    f += 1
                    if f == len(egg):
                        import life
                        life.start()
                        egg = [-1]
                else:
                    f = 0
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
        for i in range(len(rects)):
            if rects[i][0].left <= mousex <= rects[i][0].left + rects[i][0].width and \
                    rects[i][0].top <= mousey <= rects[i][0].top + rects[i][0].height:
                color = "red"
            else:
                color = "blue"
            pygame.draw.rect(screen, "white",
                             (rects[i][0].left - 1, rects[i][0].top - 1,
                              rects[i][0].width + 2, rects[i][0].height + 2))

            pygame.draw.rect(screen, color, (rects[i][0].left, rects[i][0].top,
                                             rects[i][0].width, rects[i][0].height))
            screen.blit(*texts[i])
        pygame.display.flip()
        clock.tick(FPS)


def start(*args):
    global Board, SelectImage, generate_level, maximum

    global volume
    global left, top, fon, fonplus, selected_cell, chosen_cell, FPS
    left, top = 125, 100
    FPS = 50
    selected_cell = [-500, -500]
    chosen_cell = [-500, -500]
    try:
        lines = open("settings.txt", encoding="utf8", mode="r").readlines()
        volume = 100
        for line in lines:
            if "volume=" == line[:7]:
                volume = int(line[7:])
                if not (0 <= volume <= 100):
                    volume = 100
                break
    except Exception:
        volume = 100
    Board, SelectImage, generate_level = args
    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    fonplus = pygame.transform.scale(load_image('fonplus.png'), (300, 150))

    return start_screen()
