import pygame
import pygame.gfxdraw

import functions
import play
from const import *
from play import *
from functions import *
from pygame.locals import *


def start():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    button_play = functions.Button(360, 320, 245, 55, ("Играть", 415, 315))  # создание кнопок
    running = True
    start_play = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.pressed(event.pos):
                    start_play = True

        screen.blit(functions.load_image("fon.jpg"), (0, 0))
        button_play.draw_button(screen, 0, 100)
        button_play.write(screen, COLOR_TEXT, 40)

        pygame.display.flip()

        if start_play:
            running = False
            play.start_playing(1, TEXT_TARGET_1)

    pygame.quit()


if __name__ == "__main__":
    start()