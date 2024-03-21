import pygame
import os
import sys
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


def download_image():
    db = sqlite3.connect("db/words.db")
    sql = db.cursor()
    ru = [el[0] for el in sql.execute(f"""SELECT ru FROM lets_go""").fetchall()]
    en = [el[0] for el in sql.execute(f"""SELECT en FROM lets_go""").fetchall()]
    file_image = [el[0] for el in sql.execute(f"""SELECT image FROM lets_go""").fetchall()]
    file_sound = [el[0] for el in sql.execute(f"""SELECT sound FROM lets_go""").fetchall()]
    db.close()
    return ru, en, file_image, file_sound


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

