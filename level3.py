import pygame
import pygame.gfxdraw
import random
import string
from pygame.locals import *

import functions
import main
import play
from const import *
from main import *
from play import *


class New_object(pygame.sprite.Sprite):
    def __init__(self, image, size, x, y, word_dict):
        super().__init__(photo_sprite)
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect().move(x, y)
        self.word_dict = word_dict

    def get_let_first(self):
        for i in self.word_dict.keys():
            if not self.word_dict[i]:
                return i
        return None

    def change_word(self, index):
        self.word_dict[index] = True


class WindowForWord(pygame.sprite.Sprite):
    def __init__(self, x, y, index):
        super().__init__(windows_spites)
        self.image = pygame.Surface((50, 50))
        self.image.fill(COLOR_FON_1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.coef = 1
        self.index = index
        self.letter = None
        self.can_word = None

    def draw_window(self, screen):
        rect = pygame.Rect((self.rect.x, self.rect.y, 50, 50))
        surface = pygame.Surface((50, 50), flags=SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 60 * self.coef), surface.get_rect(), border_radius=10)
        screen.blit(surface, rect)
        pygame.draw.rect(screen, COLOR_FON_1, (self.rect.x, self.rect.y, 50, 50), 2, border_radius=10)
        if self.can_word:
            font = pygame.font.SysFont("comicsansms", 35)
            string_rendered = font.render(self.letter, 1, pygame.Color(COLOR_FON))
            rect_w = string_rendered.get_rect()
            rect_w.x, rect_w.y = self.rect.x + 10, self.rect.y
            screen.blit(string_rendered, rect_w)

    def add_letter(self, letter):
        self.letter = letter

    def show_letter(self):
        return self.letter

    def is_letter(self):
        return self.can_word

    def exam(self):
        if pygame.sprite.spritecollideany(self, letters_sprites):
            return True

    def draw_letter(self):
        self.can_word = True
        self.coef = 2.5

        sprite = photo_sprite.sprites()[0]
        sprite.change_word(self.index)


class Letter(pygame.sprite.Sprite):

    def __init__(self, x, y, text):
        super().__init__(letters_sprites)

        font = pygame.font.SysFont("comicsansms", 35)
        self.text = text
        self.rect = pygame.Rect((x - 10, y, 50, 50))
        self.rect.x, self.rect.y = x, y
        self.start_x, self.start_y = x, y
        self.string_rendered = font.render(self.text, 1, pygame.Color(COLOR_FON))
        self.rect_let = self.string_rendered.get_rect()
        self.rect_let.x, self.rect_let.y = self.rect.x + 10, self.rect.y


    def write(self, screen):
        surface = pygame.Surface((50, 50), flags=SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 90), surface.get_rect(), border_radius=10)
        screen.blit(surface, self.rect)
        pygame.draw.rect(screen, COLOR_FON_1, (self.rect.x, self.rect.y, 50, 50), 2, border_radius=10)
        screen.blit(self.string_rendered, self.rect_let)

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self, pos):
        self.rect.x, self.rect.y = pos[0] - len(self.text) * 15, pos[1] - 20
        self.rect_let.x, self.rect_let.y = pos[0] - len(self.text) * 5, pos[1] - 20

    def return_coords(self):
        self.rect.x, self.rect.y = self.start_x, self.start_y
        self.rect_let.x, self.rect_let.y = self.start_x + 10, self.start_y

    def show_letter(self):
        return self.text


def now_word(images, en_words):
    num = random.randint(0, len(images) - 1)
    image, word = images[num], en_words[num]
    images.pop(num)
    en_words.pop(num)
    return image, list(word.upper()), images, en_words


def create_all(word, image):
    word_dict = {}
    for w in range(len(word)):
        word_dict[w] = False
    New_object(functions.load_image(image, colorkey=1),  350, 340, 70, word_dict)

    x = (WIDTH_SCREEN - (50 * len(word) + 50 * (len(word) - 1))) // 2
    for i in range(len(word)):
        WindowForWord(x, 470, i)
        windows_spites.sprites()[i].add_letter(word[i])
        x += 100

    max_letters = len(word) + 3 if len(word) <= 5 else len(word) + 2
    list_letters = list(word)
    add_list_words = random.sample(string.ascii_letters[0:len(string.ascii_letters) // 2], max_letters)
    while len(list_letters) < max_letters:
        list_letters.append(add_list_words[0])
        add_list_words.pop(0)
    random.shuffle(list_letters)
    x = (WIDTH_SCREEN - (50 * len(list_letters) + 30 * (len(list_letters) - 1))) // 2 + 40
    for letter in list_letters:
        Letter(x, 580, letter.upper())
        x += 70


def update_all():
    for sprite in windows_spites:
        sprite.kill()
    for sprite in photo_sprite:
        sprite.kill()
    for sprite in letters_sprites:
        sprite.kill()


def help(word):
    index = photo_sprite.sprites()[0].get_let_first()
    if index != None:
        for sprite_window in windows_spites:  # если еще выбрано, проверяем находится ли оно в том окне
            sprite_window.is_letter()
            if sprite_window.show_letter() == word[index] and not sprite_window.is_letter():
                sprite_window.draw_letter()
                for sprite_down in letters_sprites.sprites():
                    if sprite_down.show_letter() == word[index]:
                        letters_sprites.remove(sprite_down)
                        break
                break
        return index
    return None


def level_3():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    button_back = functions.Button(25, 20, 125, 40, ("Выйти", 45, 20))
    button_help = functions.Button(740, 20, 180, 40, ("Подсказка", 760, 20))
    button_next = None
    pressed_sprite = None

    running = True
    backing = False
    pressed = False
    pressed_word = False
    next_words = False
    next_level = False

    en_words, list_image_files, list_sound_files = functions.open_file_words()
    image, word, list_image_files, en_words = now_word(list_image_files, en_words)
    eternal_word = word[::]
    create_all(word, image)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.pressed(event.pos):
                    backing = True

                if button_help.pressed(event.pos):
                    index = help(eternal_word)
                    if index != None:
                        word.remove(eternal_word[index])

                if next_words and button_next.pressed(event.pos):
                    if len(en_words) > 0:
                        update_all()
                        image, word, list_image_files, en_words = now_word(list_image_files, en_words)
                        eternal_word = word[::]
                        create_all(word, image)
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

        screen.blit(functions.load_image("fon3.jpg"), (0, 0))

        button_back.draw_button(screen, 0, 110)
        button_back.write(screen, COLOR_TEXT_1, 27)
        button_help.draw_button(screen, 0, 110)
        button_help.write(screen, COLOR_TEXT_1, 27)
        if next_words:
            button_next.draw_button(screen, 0, 90)
            button_next.write(screen, COLOR_TEXT_1, 27)

        # рисование квадрат под картинкой
        rect = pygame.Rect(330, 70, 360, 360)
        surface = pygame.Surface((360, 360), flags=SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 80), surface.get_rect(), border_radius=30)
        screen.blit(surface, rect)

        photo_sprite.draw(screen)

        for sprite in windows_spites:  # рисование окошек для слов
            sprite.draw_window(screen)

        for sprite in letters_sprites:  # рисование слов
            sprite.write(screen)

        if pressed:  # если пользователь зажал кнопку мыши, проверяем нажал ли он на какой-нибудь слово
            if not pressed_word:  # если нет
                for sprite_let in letters_sprites:  # перебираем все слова и проверяем нажал ли на них пользователь
                    if sprite_let.is_clicked():
                        pressed_word = True
                        pressed_sprite = sprite_let

            else:
                pressed_sprite.update(mouse_pos)  # если пользователь уже нажал на слово, то двигаем слово за курсором

        else:
            if pressed_word:  # если кнопка мыши уже не зажата, то проверяем выбрано ли еще слово
                for sprite_window in windows_spites:  # если еще выбрано, проверяем находится ли оно в том окне
                    if sprite_window.exam() and sprite_window.show_letter() == pressed_sprite.show_letter():
                        sprite_window.draw_letter()
                        word.remove(pressed_sprite.show_letter())
                        pressed_sprite.kill()

                pressed_sprite.return_coords()  # если ползователь перенес слово неправильно, возвращаем слово в начальное положение
                pressed_word = False


        if len(word) == 0:
            next_words = True
            if len(en_words) == 0:
                button_next = functions.Button(650, 630, 305, 45, ("Следующий уровень", 670, 630))
            else:
                button_next = functions.Button(770, 630, 200, 45, ("Следующие", 790, 630))

        pygame.display.flip()

        if backing:
            running = False
            main.start()
        if next_level:
            running = False
            play.start_playing(4, TEXT_TARGET_3)

    pygame.quit()

windows_spites = pygame.sprite.Group()
photo_sprite = pygame.sprite.Group()
letters_sprites = pygame.sprite.Group()

if __name__ == "__main__":
    level_3()