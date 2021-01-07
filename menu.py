import sys
import os
from pprint import pprint
from random import randrange
import random
import pygame


'''def training():
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
        clock.tick(FPS)'''


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
                        volume = int(x / 440 * 100)
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

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 10
    rects = []
    texts = []
    for line, cmd in buttons:
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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, f in enumerate(rects):
                    rect, cmd = f
                    if rect.left <= event.pos[0] <= rect.left + rect.width and\
                            rect.top <= event.pos[1] <= rect.top + rect.height:
                        if cmd == "exit":
                            return i + 2
                        return cmd()
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
        for i, f in enumerate(rects):
            rect, cmd = f
            if rect.left <= mousex <= rect.left + rect.width and\
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
               ("Настройки", settings)]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 10
    rects = []
    texts = []
    for line, cmd in buttons:
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
            if rects[i][0].left <= mousex <= rects[i][0].left + rects[i][0].width and\
                    rects[i][0].top <= mousey <= rects[i][0].top + rects[i][0].height:
                color = "red"
            else:
                color = "blue"
            pygame.draw.rect(screen, "white",
                             (rects[i][0].left - 1, rects[i][0].top - 1, rects[i][0].width + 2, rects[i][0].height + 2))
            pygame.draw.rect(screen, color, (rects[i][0].left, rects[i][0].top, rects[i][0].width, rects[i][0].height))
            screen.blit(*texts[i])
        pygame.display.flip()
        clock.tick(FPS)


def start(*args):
    global screen, width, height, clock, FPS, terminate, load_image  # Общие переменные(импортируются)
    global volume  # Возвращаемые переменные
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
    screen, width, height, clock, FPS, terminate, load_image = args
    return start_screen()
