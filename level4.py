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


class New_object(pygame.sprite.Sprite):
    def __init__(self, image, size, x, y):
        super().__init__(photo_sprite)
        self.size = size
        self.x, self.y = x, y
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect().move(x, y)


    def change_img(self, img):
        self.image = pygame.transform.scale(functions.load_image(img, colorkey=1), (self.size, self.size))
        self.rect = self.image.get_rect().move(self.x, self.y)


class WindowForWord(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(windows_spites)
        self.image = pygame.Surface((200, 50))
        self.image.fill(COLOR_FON_1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.coef = 1
        self.plus = 0
        self.word = None
        self.can_word = None

    def draw_window(self, screen):
        rect = pygame.Rect((self.rect.x, self.rect.y, 270, 50))
        surface = pygame.Surface((270, 50), flags=SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 60 * self.coef), surface.get_rect(), border_radius=30)
        screen.blit(surface, rect)
        pygame.draw.rect(screen, COLOR_FON_1, (self.rect.x, self.rect.y, 270, 50), 2, border_radius=30)
        if self.can_word:
            font = pygame.font.SysFont("comicsansms", 35)
            string_rendered = font.render(self.word, 1, pygame.Color(COLOR_FON))
            rect_w = string_rendered.get_rect()
            rect_w.x, rect_w.y = self.rect.x + self.plus, self.rect.y - 5
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
        self.coef = 2.5
        self.plus = (270 - 20 * len(self.word)) // 2


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


def now_word(images, en_words, sounds):
    num = random.randint(0, len(images) - 1)
    image, word, sound = images[num], en_words[num],  sounds[num]
    images.pop(num)
    en_words.pop(num)
    sounds.pop(num)
    return image, word, sound, images, en_words, sounds


def create_all(en_words, word, img):
    New_object(functions.load_image(img, colorkey=1), 300, 355, 80)
    WindowForWord(370, 400)
    windows_spites.sprites()[0].add_word(word)

    list_words = set()
    list_words.add(word)
    add_list_words = random.sample(en_words, 5)
    while len(list_words) < 5:
        list_words.add(add_list_words[0])
        add_list_words.pop(0)

    plus_x = 20
    for word in list_words:
        Word(140 + plus_x, 540, word)
        plus_x += 150

    return list_words


def start_sound(mus):
    sound = pygame.mixer.Sound(f"sounds/{mus}")
    sound.play()


def update_all():
    for sprite in windows_spites:
        sprite.kill()
    for sprite in photo_sprite:
        sprite.kill()
    for sprite in words_sprites:
        sprite.kill()


def level_4():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    button_back = functions.Button(25, 20, 125, 40, ("Выйти", 45, 20))
    button_not_sound = functions.Button(730, 20, 250, 40, ("Не могу слушать", 745, 20))
    button_next = None

    pressed_sprite = None

    running = True
    backing = False
    pressed = False
    pressed_word = False
    next_words = False
    end = False

    but_sound = functions.Button(260, 90, 70, 70, ("", 0, 0))
    image = pygame.image.load("images/but_sound.png")
    button_sound = pygame.transform.scale(image, (70, 70))
    but_rect = button_sound.get_rect().move(260, 90)

    en_words, list_image_files, list_sound_files = functions.open_file_words()
    all_en_words = en_words[::]
    image, word, sound, list_image_files, en_words, list_sound_files = now_word(list_image_files,
                                                                                en_words, list_sound_files)
    list_now_words = create_all(all_en_words, word, "img_question.png")
    start_sound(sound)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.pressed(event.pos):
                    backing = True
                if but_sound.pressed(event.pos):
                    start_sound(sound)
                if button_not_sound.pressed(event.pos):
                    end = True
                if next_words and button_next.pressed(event.pos):
                    if len(en_words) > 0:
                        update_all()
                        image, word, sound, list_image_files, en_words, list_sound_files = now_word(list_image_files,
                                                                              en_words, list_sound_files)
                        list_now_words = create_all(all_en_words, word, "img_question.png")
                        start_sound(sound)
                        button_next = None
                        next_words = False
                    else:
                        end = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pressed = False

        mouse_pos = pygame.mouse.get_pos()  # получение координаты мыши

        screen.blit(functions.load_image("fon4.jpg"), (0, 0))

        # рисование квадрат под картинкой
        rect = pygame.Rect(350, 70, 310, 310)
        surface = pygame.Surface((310, 310), flags=SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 80), surface.get_rect(), border_radius=30)
        screen.blit(surface, rect)

        # рисование кнопок
        button_back.draw_button(screen, 0, 100)
        button_back.write(screen, COLOR_TEXT_1, 27)
        button_not_sound.draw_button(screen, 0, 100)
        button_not_sound.write(screen, COLOR_TEXT_1, 27)
        if next_words:
            button_next.draw_button(screen, 0, 110)
            button_next.write(screen, COLOR_TEXT_1, 27)
            photo_sprite.sprites()[0].change_img(image)

        # рисование квадрат под словами
        rect = pygame.Rect(70, 530, 870, 90)
        surface = pygame.Surface((870, 80), flags=SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 125), surface.get_rect(), border_radius=30)
        screen.blit(surface, rect)

        photo_sprite.draw(screen)
        windows_spites.sprites()[0].draw_window(screen)
        screen.blit(button_sound, but_rect)

        for sprite in words_sprites:  # рисование слов
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
                        next_words = True

                pressed_sprite.return_coords()  # если ползователь перенес слово неправильно, возвращаем слово в начальное положение
                pressed_word = False


        if len(list_now_words) == 4:
            if len(en_words) == 0:
                button_next = functions.Button(760, 630, 190, 45, ("Закончить", 790, 630))
            else:
                button_next = functions.Button(770, 630, 200, 45, ("Следующий", 790, 630))
                next_words = True

        pygame.display.flip()

        if backing:
            running = False
            main.start()
        if end:
            running = False
            play.last_screen()

    pygame.quit()


photo_sprite = pygame.sprite.Group()
windows_spites = pygame.sprite.Group()
words_sprites = pygame.sprite.Group()

if __name__ == "__main__":
    level_4()