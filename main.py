import pygame
import pygame.gfxdraw
import json

import functions
import play
from const import *
from play import *
from functions import *
from pygame.locals import *


class ButtonLevel(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, book, text):
        super().__init__(all_buttons_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.book = book
        self.text = text

    # отрисовка надписи на кнопке
    def write(self, screen, size_font):
        font = pygame.font.SysFont("comicsansms", size_font)
        x, y = self.rect.x - 10, self.rect.y + 180
        for line in self.text:
            string_rendered = font.render(line, 1, pygame.Color(COLOR_FON))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = x
            intro_rect.y = y
            screen.blit(string_rendered, intro_rect)  # отрисовка номера уровня
            y += 20
            x += 25

    def write2(self, screen, size_font):
        rect = pygame.Rect((self.rect.x, self.rect.y, self.rect.w, self.rect.h))
        surface = pygame.Surface((self.rect.w, self.rect.h), flags=SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 130), surface.get_rect(), border_radius=10)
        screen.blit(surface, rect)

        font = pygame.font.SysFont("comicsansms", size_font)
        x, y = self.rect.x + 10, self.rect.y + 25
        for line in self.text[1::]:
            string_rendered = font.render(line, 1, pygame.Color(COLOR_FON))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = x
            intro_rect.y = y
            screen.blit(string_rendered, intro_rect)  # отрисовка номера уровня
            y += 25
            x += 10

    # нажатие кнопки
    def pressed(self, mouse):
        if self.rect.x <= mouse[0] <= self.rect.x + self.rect.w and\
                self.rect.y <= mouse[1] <= self.rect.y + self.rect.h:
            return self.book


def start():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    button_play = functions.Button(530, 490, 245, 55, ("Начать", 585, 485))  # создание кнопок
    font = pygame.font.SysFont("comicsansms", 70)

    picture = functions.load_image('fon_text.png', (690, 450))
    text_rect = picture.get_rect().move(280, 70)
    picture.set_alpha(80)

    str_name = font.render('CatSpeak', 1, pygame.Color(COLOR_FON))
    rect_name = str_name.get_rect()
    rect_name.x, rect_name.y = 330, 20

    image_cat = functions.load_image('cat_fon.png', (600, 600))
    cat_rect = image_cat.get_rect().move(-90, 130)

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
        screen.blit(picture, text_rect)
        screen.blit(str_name, rect_name)
        screen.blit(image_cat, cat_rect)

        button_play.draw_button(screen, 0, 150)
        button_play.write(screen, COLOR_TEXT_1, 40)

        y = 155
        font = pygame.font.SysFont("comicsansms", 20)
        for text in TEXT_HELLO:
            string_rendered = font.render(text, 1, pygame.Color(COLOR_FON))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 420
            intro_rect.y = y
            screen.blit(string_rendered, intro_rect)
            y += 25

        pygame.display.flip()

        if start_play:
            running = False
            choose_book()

    pygame.quit()


def choose_book():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    button_back = functions.Button(25, 20, 125, 40, ("Назад", 45, 20))

    create_buttons_books()

    book = None
    running = True
    next = False
    back = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.pressed(event.pos):
                    back = True

                for sprite in all_buttons_sprites:
                    result = sprite.pressed(event.pos)
                    if result:
                        book = result
                        next = True

        screen.blit(functions.load_image("fon.jpg"), (0, 0))

        font = pygame.font.SysFont("comicsansms", 50)
        string_rendered = font.render('Выбери учебник', 1, pygame.Color(COLOR_FON))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = 310, 35
        screen.blit(string_rendered, intro_rect)  # отрисовка номера уровня

        button_back.draw_button(screen, 0, 90)
        button_back.write(screen, COLOR_TEXT_1, 27)

        all_buttons_sprites.draw(screen)
        for sprite in all_buttons_sprites:
            sprite.write(screen, 15)

        pygame.display.flip()
        if next:
            clear()
            running = False
            choose_topic(book)
        if back:
            clear()
            running = False
            start()

    pygame.quit()


def choose_topic(book):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    button_start = functions.Button(700, 600, 245, 55, ("Начать", 750, 595))  # создание кнопок
    button_back = functions.Button(25, 20, 125, 40, ("Назад", 45, 20))

    topics = json.load(open('words.json'))[book]
    create_buttons_topics(topics)

    data = None
    running = True
    start_play = False
    back = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.pressed(event.pos):
                    start_play = True
                if button_back.pressed(event.pos):
                    back = True

                for sprite in all_buttons_sprites:
                    result = sprite.pressed(event.pos)
                    if result:
                        functions.download(result[0])
                        start_play = True

        screen.blit(functions.load_image("fon.jpg"), (0, 0))

        font = pygame.font.SysFont("comicsansms", 50)
        string_rendered = font.render('Выбери тему', 1, pygame.Color(COLOR_FON))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = 340, 35
        screen.blit(string_rendered, intro_rect)  # отрисовка номера уровня

        button_back.draw_button(screen, 0, 90)
        button_back.write(screen, COLOR_TEXT_1, 27)

        for sprite in all_buttons_sprites:
            sprite.write2(screen, 17)

        pygame.display.flip()

        if start_play:
            clear()
            running = False
            play.start_playing(1, TEXT_TARGET_1)
        if back:
            clear()
            running = False
            choose_book()

    pygame.quit()


def clear():
    for sprite in all_buttons_sprites:
        sprite.kill()


def create_buttons_topics(topics):
    x, y = 55, 140
    for i in range(len(topics)):
        ButtonLevel(pygame.Surface((110, 100)), x, y, topics[i], topics[i])
        if i == 6:
            x = 55
            y = 260
        else:
             x += 130


def create_buttons_books():
    list_books = {'book_2_1.png': ['Spotlight, Быкова Н.И', '2 класс 1 часть'], 'book_2_2.png': ['Spotlight, Быкова Н.И', '3 класс 2 часть'],
                  'book_3_1.jpg': ['Spotlight, Быкова Н.И', '3 класс 1 часть'], 'book_3_2.jpg': ['Spotlight, Быкова Н.И', '3 класс 2 часть']}
    x, y = 100, 140
    for book in list_books:
        ButtonLevel(functions.load_image(book, (130, 170)), x, y, book, list_books[book])
        x += 190

all_buttons_sprites = pygame.sprite.Group()

if __name__ == "__main__":
    start()