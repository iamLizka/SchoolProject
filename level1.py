import pygame
import pygame.gfxdraw
from pygame.locals import *

import functions
import main
import play
from const import *
from main import *
from functions import *
from play import *


class New_object(pygame.sprite.Sprite):
    def __init__(self, image, size, x, y):
        super().__init__(photo_sprite)
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect().move(x, y)


def start_sound(list_sounds):
    sound = pygame.mixer.Sound(f"sounds/{list_sounds[0]}")
    sound.play()


def output_word(screen, word):
    font = pygame.font.SysFont("comicsansms", 50)
    string_rendered = font.render(word, 1, pygame.Color(COLOR_FON))
    intro_rect = string_rendered.get_rect()
    intro_rect.x, intro_rect.y = (WIDTH_SCREEN - (30 * len(word))) // 2, 510
    screen.blit(string_rendered, intro_rect)


def delete_image_word(en, files_image, files_sound):
    if len(en) == 1:
        return False
    photo_sprite.sprites()[0].kill()
    for list_ in [en, files_image, files_sound]:
        list_.pop(0)
    New_object(functions.load_image(files_image[0], colorkey=1), 370, 320, 100)
    start_sound(files_sound)

    return en, files_image, files_sound


def choose_image_word(en, files_img, files_sound):
    photo_sprite.sprites()[0].kill()

    for list_ in [en, files_img, files_sound]:
        list_.append(list_.pop(0))
    New_object(functions.load_image(files_img[0], colorkey=1), 370, 320, 100)
    start_sound(files_sound)

    return en, files_img, files_sound


def level_1():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    button_next = functions.Button(770, 595, 165, 55, ("Дальше", 795, 600))
    button_back = functions.Button(25, 20, 125, 40, ("Выйти", 45, 20))
    button_repeat = functions.Button(25, 595, 195, 55, ("Повторить", 45, 600))

    but_sound = functions.Button(180, 120, 60, 60, ("", 0, 0))
    image = pygame.image.load("images/but_sound.png")
    button_sound = pygame.transform.scale(image, (60, 60))
    but_rect = button_sound.get_rect().move(180, 120)

    running = True
    backing = False
    next = False
    next_level = False

    en_words, list_image_files, list_sound_files = functions.open_file_words()
    New_object(functions.load_image(list_image_files[0], colorkey=1), 370, 320, 100)
    start_sound(list_sound_files)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_next.pressed(event.pos):
                    data = delete_image_word(en_words, list_image_files, list_sound_files)
                    if not data:
                        if not next_level:
                            button_next = functions.Button(650, 595, 320, 55, ("Следующий уровень", 665, 600))
                            next_level = True
                        else:
                            next = True
                    else:
                        en_words, list_image_files, list_sound_files = data
                if button_repeat.pressed(event.pos):
                    en_words, list_image_files, list_sound_files = choose_image_word(en_words, list_image_files, list_sound_files)
                if button_back.pressed(event.pos):
                    backing = True
                if but_sound.pressed(event.pos):
                    start_sound(list_sound_files)

        screen.blit(functions.load_image("fon1.jpg"), (0, 0))
        rect = pygame.Rect((250, 100, 600, 500))
        surface = pygame.Surface((500, 400), flags=SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 130), surface.get_rect(), border_radius=30)
        screen.blit(surface, rect)
        screen.blit(button_sound, but_rect)

        output_word(screen, en_words[0])

        photo_sprite.draw(screen)
        button_next.draw_button(screen, 0, 90)
        button_next.write(screen, COLOR_TEXT_1, 30)
        button_back.draw_button(screen, 0, 90)
        button_back.write(screen, COLOR_TEXT_1, 27)
        button_repeat.draw_button(screen, 0, 90)
        button_repeat.write(screen, COLOR_TEXT_1, 30)

        pygame.display.flip()

        if backing:
            running = False
            for sprite in photo_sprite:
                sprite.kill()
            main.start()
        if next:
            running = False
            play.start_playing(2, TEXT_TARGET_2)

    pygame.quit()

photo_sprite = pygame.sprite.Group()


# if __name__ == "__main__":
#     level_1()

