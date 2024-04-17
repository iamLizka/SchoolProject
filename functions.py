import pygame
import os
import sys
import json
import sqlite3
from const import *
from level1 import *
from level2 import *
from pygame.locals import *


"""загрузка изображения"""
def load_image(name, size=None, colorkey=None):
    fullname = os.path.join('images', name)
    # проверяем существует ли такой файл
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # при необходимости убираем фон
    if colorkey is not None:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    if size:
        image = pygame.transform.scale(image, (size[0], size[1]))
    return image


def download(topic):
    db = sqlite3.connect("db/words.db")
    sql = db.cursor()
    data = {}
    en = [el[0] for el in sql.execute(f"""SELECT en FROM {topic}""").fetchall()]
    file_image = [el[0] for el in sql.execute(f"""SELECT image FROM {topic}""").fetchall()]
    file_sound = [el[0] for el in sql.execute(f"""SELECT sound FROM {topic}""").fetchall()]
    db.close()
    data["en"] = en
    data["images"] = file_image
    data["sounds"] = file_sound
    with open('now_words.json', 'w') as file:
        json.dump(data, file)


def open_file_words():
    with open('now_words.json') as file:
        data = json.load(file)
        en_words = data['en']
        list_image_files = data['images']
        list_sound_files = data['sounds']
        return en_words, list_image_files, list_sound_files


class Button:
    def __init__(self, x, y, width, height, data_text=None):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = COLOR_TEXT
        if data_text:
            self.text = data_text[0]
            self.text_x, self.text_y = data_text[1], data_text[2]

    # отрисовка кнопки
    def draw_button(self, screen, color, trans):
        rect = pygame.Rect((self.x, self.y, self.width, self.height))
        surface = pygame.Surface((self.width, self.height), flags=SRCALPHA)
        if color:
            pygame.draw.rect(surface, (255, 255, 255, trans), surface.get_rect(), border_radius=30)
        else:
            pygame.draw.rect(surface, (0, 0, 0, trans), surface.get_rect(), border_radius=30)
        screen.blit(surface, rect)

    # отрисовка надписи
    def write(self, screen, color, size_font):
        font = pygame.font.SysFont("comicsansms", size_font)
        string_rendered = font.render(self.text, 1, pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = self.text_x
        intro_rect.y = self.text_y
        screen.blit(string_rendered, intro_rect)

    # нажатие кнопки
    def pressed(self, mouse):
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            return True

