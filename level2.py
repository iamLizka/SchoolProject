import pygame
import pygame.gfxdraw
import random
from pygame.locals import *

import functions
import main
import play
from const import *
from main import *
from play import *

class WindowForWord(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(windows_spites)
        self.image = pygame.Surface((200, 40))
        self.image.fill(COLOR_FON_1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.word = None
        self.can_word = None

    def draw_window(self, screen):
        rect = pygame.Rect((self.rect.x, self.rect.y, 200, 50))
        surface = pygame.Surface((200, 50), flags=SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 50), surface.get_rect(), border_radius=30)
        screen.blit(surface, rect)
        pygame.draw.rect(screen, COLOR_FON_1, (self.rect.x, self.rect.y, 200, 50), 2, border_radius=30)
        if self.can_word:
            font = pygame.font.SysFont("comicsansms", 35)
            string_rendered = font.render(self.word, 1, pygame.Color(COLOR_FON))
            rect_w = string_rendered.get_rect()
            rect_w.x, rect_w.y = self.rect.x + 100 - len(self.word) * 17 // 2, self.rect.y - 4
            screen.blit(string_rendered, rect_w)

    def add_word(self, word):
        self.word = word

    def show_word(self):
        return self.word

    def exam(self):
        if pygame.sprite.spritecollideany(self, words_sprites):
            return True

    def draw_word(self):
        self.can_word = True



class Word(pygame.sprite.Sprite):

    def __init__(self, x, y, text):
        super().__init__(words_sprites)

        font = pygame.font.SysFont("comicsansms", 33)
        self.x, self.y = x, y
        self.start_x, self.start_y = x, y
        self.text = text
        self.string_rendered = font.render(self.text, 1, pygame.Color(COLOR_FON))
        self.rect = self.string_rendered.get_rect()
        self.rect.x, self.rect.y = x, y

    def write(self, screen):
        screen.blit(self.string_rendered, self.rect)

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self, pos):
        self.rect.x, self.rect.y = pos[0] - len(self.text) * 7, pos[1] - 20

    def return_coords(self):
        self.rect.x, self.rect.y = self.x, self.y

    def show_word(self):
        return self.text


class New_object(pygame.sprite.Sprite):
    def __init__(self, image, size, x, y):
        super().__init__(object_sprite)
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect().move(x, y)


def level_2():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    button_back = functions.Button(25, 20, 125, 40, ("Выйти", 45, 20))
    button_next = None

    pressed_sprite = None

    running = True
    backing = False
    pressed = False
    pressed_word = False
    next_words = False
    next_level = False

    ru_words, en_words, list_image_files, list_sound_files = functions.download_image()
    all_en_words = en_words[::]
    count_img = count_image(len(en_words))
    coord_x = coord_x_for_img(len(en_words))

    list_now_words = create_all(count_img, list_image_files, coord_x, en_words, all_en_words)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.pressed(event.pos):
                    backing = True

                if next_words and button_next.pressed(event.pos):
                    en_words, list_image_files = update_window(en_words, list_image_files)
                    count_img = count_image(len(en_words))
                    if count_img:
                        coord_x = coord_x_for_img(len(en_words))
                        list_now_words = create_all(count_img, list_image_files, coord_x, en_words, all_en_words)
                        button_next = None
                        next_words = False
                    else:
                        next_level = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pressed = False

        mouse_pos = pygame.mouse.get_pos()  # получение координаты мыши

        screen.blit(functions.load_image("fon1.jpg"), (0, 0))

        # рисование кнопок
        button_back.draw_button(screen, 0, 90)
        button_back.write(screen, COLOR_TEXT_1, 27)
        if next_words:
            button_next.draw_button(screen, 0, 90)
            button_next.write(screen, COLOR_TEXT_1, 27)

        # рисование квадрат под словами
        rect = pygame.Rect(70, 530, 870, 90)
        surface = pygame.Surface((870, 80), flags=SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 125), surface.get_rect(), border_radius=30)
        screen.blit(surface, rect)

        object_sprite.draw(screen)  # рисование картинок

        for sprite in windows_spites:  # рисование окошек для слов
            sprite.draw_window(screen)

        for sprite in words_sprites:  #  рисование слов
            sprite.write(screen)

        if pressed:  # если пользователь зажал кнопку мыши, проверяем нажал ли он на какой-нибудь слово
            if not pressed_word:  # если нет
                for sprite_word in words_sprites:  # перебираем все слова и проверяем нажал ли на них пользователь
                    if sprite_word.is_clicked():
                        pressed_word = True
                        pressed_sprite = sprite_word

            else:
                pressed_sprite.update(mouse_pos)  # если пользователь уже нажал на слово, то двигаем слово за курсором

        else:
            if pressed_word:  # если кнопка мыши уже не зажата, то проверяем выбрано ли еще слово
                for sprite_window in windows_spites:  # если еще выбрано, проверяем находится ли оно в том окне
                    if sprite_window.exam() and sprite_window.show_word() == pressed_sprite.show_word():
                        sprite_window.draw_word()
                        list_now_words.remove(pressed_sprite.show_word())
                        pressed_sprite.kill()

                pressed_sprite.return_coords()  # если ползователь перенес слово неправильно, возвращаем слово в начальное положение
                pressed_word = False

        if 5 - count_img == len(list_now_words):
            next_words = True
            if not count_image(len(en_words) - count_img):
                button_next = functions.Button(650, 630, 305, 45, ("Следующий уровень", 670, 630))
            else:
                button_next = functions.Button(770, 630, 200, 45, ("Следующие", 790, 630))

        pygame.display.flip()

        if backing:
            running = False
            # for sprite in object_sprite:
            #     sprite.kill()
            main.start()
        if next_level:
            running = False
            play.start_playing(3, TEXT_TARGET_2)

    pygame.quit()


def create_all(count, list_img, coord_x, en_words, all_en_words):
    plus_x = 20
    for i in range(count):
        WindowForWord(coord_x + plus_x, 380)
        plus_x += 310

    plus_x = 0
    for i in range(count):
        New_object(functions.load_image(list_img[i], colorkey=1), 230, coord_x + plus_x, 110)
        windows_spites.sprites()[i].add_word(en_words[i])
        plus_x += 310

    list_words = set(en_words[:3])
    add_list_words = random.sample(all_en_words, 5)
    while len(list_words) < 5:
        list_words.add(add_list_words[0])
        add_list_words.pop(0)

    plus_x = 20
    for word in list_words:
        Word(140 + plus_x, 540, word)
        plus_x += 150

    return list_words


def count_image(count):
    if count <= 0:
        return False
    count_img = 3 if count >= 3 else count % 3
    return count_img

def coord_x_for_img(count):
    x = 300 if count == 1 else 200
    x = 80 if count >= 3 else 200
    return x

def update_window(en_words, images):
    for sprite in object_sprite:
        sprite.kill()
    for sprite in windows_spites:
        sprite.kill()
    for sprite in words_sprites:
        sprite.kill()

    en_words = en_words[3:] if len(en_words) >= 3 else en_words[len(en_words):]
    images = images[3:] if len(images) >= 3 else images[len(images):]

    return en_words, images


object_sprite = pygame.sprite.Group()
windows_spites = pygame.sprite.Group()
words_sprites = pygame.sprite.Group()

if __name__ == "__main__":
    level_2()


