import pygame
import pygame.gfxdraw
import functions
import level1
import level2
import level3
import level4
import main

from const import *
from main import *
from functions import *
from pygame.locals import *


def start_playing(level, target):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    button_back = functions.Button(25, 20, 125, 40, ("Выйти", 45, 20))
    button_start = functions.Button(600, 490, 170, 55, ("Начать", 625, 490))

    for_text = pygame.image.load("images/fon_text.png")
    picture = pygame.transform.scale(for_text, (700, 540))
    text_rect = picture.get_rect().move(270, -20)
    picture.set_alpha(80)

    font = pygame.font.SysFont("comicsansms", 30)
    num_level = font.render(f"Уровень {level}", 1, pygame.Color(COLOR_FON))
    num_rect = num_level.get_rect()
    num_rect.x, num_rect.y = 540, 95

    font = pygame.font.SysFont("comicsansms", 25)

    running = True
    backing = False
    start_1 = False
    start_2 = False
    start_3 = False
    start_4 = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.pressed(event.pos):
                    backing = True
                if button_start.pressed(event.pos):
                    if level == 1:
                        start_1 = True
                    elif level == 2:
                        start_2 = True
                    elif level == 3:
                        start_3 = True
                    elif level == 4:
                        start_4 = True

        screen.blit(functions.load_image(f"fon{level}.jpg"), (0, 0))
        screen.blit(picture, text_rect)
        screen.blit(num_level, num_rect)

        image_cat = functions.load_image('cat_fon.png', (600, 600))
        cat_rect = image_cat.get_rect().move(-90, 130)
        screen.blit(image_cat, cat_rect)

        y = 145
        for text in target:
            string_rendered = font.render(text, 1, pygame.Color(COLOR_FON))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 420
            intro_rect.y = y
            screen.blit(string_rendered, intro_rect)
            y += 35

        button_start.draw_button(screen, 0, 100)
        button_start.write(screen, COLOR_TEXT_1, 35)
        button_back.draw_button(screen, 0, 90)
        button_back.write(screen, COLOR_TEXT_1, 27)

        pygame.display.flip()

        if backing:
            running = False
            main.start()
        if start_1:
            running = False
            level1.level_1()
        if start_2:
            running = False
            level2.level_2()
        if start_3:
            running = False
            level3.level_3()
        if start_4:
            running = False
            level4.level_4()

    pygame.quit()

def last_screen():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    button_1 = functions.Button(370, 250, 220, 50, ("1 уровень", 410, 250))
    button_2 = functions.Button(370, 310, 220, 50, ("2 уровень", 410, 310))
    button_3 = functions.Button(370, 370, 220, 50, ("3 уровень", 410, 370))
    button_4 = functions.Button(370, 430, 220, 50, ("4 уровень", 410, 430))
    button_back = functions.Button(370, 500, 220, 50, ("Выйти", 440, 505))


    font = pygame.font.SysFont("comicsansms", 70)
    text1 = font.render(f"Молодец!", 1, pygame.Color(COLOR_FON))
    text_rect1 = text1.get_rect()
    text_rect1.x, text_rect1.y = 320, 95
    font = pygame.font.SysFont("comicsansms", 25)
    text2 = font.render(f"Повторить:", 1, pygame.Color(COLOR_FON))
    text_rect2 = text2.get_rect()
    text_rect2.x, text_rect2.y = 410, 190

    running = True
    backing = False
    start_1 = False
    start_2 = False
    start_3 = False
    start_4 = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.pressed(event.pos):
                    backing = True
                if button_1.pressed(event.pos):
                    start_1 = True
                if button_2.pressed(event.pos):
                    start_2 = True
                if button_3.pressed(event.pos):
                    start_3 = True
                if button_4.pressed(event.pos):
                    start_4 = True


        screen.blit(functions.load_image(f"fon.jpg"), (0, 0))

        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)

        button_back.draw_button(screen, 0, 110)
        button_back.write(screen, COLOR_TEXT_1, 27)
        button_1.draw_button(screen, 0, 110)
        button_1.write(screen, COLOR_TEXT_1, 30)
        button_2.draw_button(screen, 0, 110)
        button_2.write(screen, COLOR_TEXT_1, 30)
        button_3.draw_button(screen, 0, 110)
        button_3.write(screen, COLOR_TEXT_1, 30)
        button_4.draw_button(screen, 0, 110)
        button_4.write(screen, COLOR_TEXT_1, 30)

        pygame.display.flip()

        if backing:
            running = False
            main.start()
        if start_1:
            running = False
            level1.level_1()
        if start_2:
            running = False
            level2.level_2()
        if start_3:
            running = False
            level3.level_3()
        if start_4:
            running = False
            level4.level_4()

    pygame.quit()


if __name__ == "__main__":
    last_screen()