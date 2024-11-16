# modules/button.py

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os

class Button:
    def __init__(self, pos, size, text, theme):
        self.pos = pos              # Позиция кнопки [x, y]
        self.size = size            # Размер кнопки [width, height]
        self.text = text            # Текст на кнопке
        self.theme = theme          # Тема оформления кнопки

        # Путь к шрифту, поддерживающему кириллицу
        self.font_path = 'assets/fonts/arial.ttf'
        self.font_size = 30  # Размер шрифта
        self.font = ImageFont.truetype(self.font_path, self.font_size)

    def draw(self, img):
        x, y = self.pos
        w, h = self.size

        # Рисуем прямоугольник кнопки
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['button_color'], cv2.FILLED)

        # Конвертируем изображение в формат PIL
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Рисуем текст на кнопке
        text_size = draw.textsize(self.text, font=self.font)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h - text_size[1]) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_color']))

        # Обратно конвертируем изображение в формат OpenCV
        img[:] = np.array(img_pil)

    def draw_hover(self, img):
        x, y = self.pos
        w, h = self.size

        # Рисуем кнопку с эффектом наведения
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['hover_color'], cv2.FILLED)

        # Конвертируем изображение в формат PIL
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Рисуем текст на кнопке
        text_size = draw.textsize(self.text, font=self.font)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h - text_size[1]) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_hover_color']))

        # Обратно конвертируем изображение в формат OpenCV
        img[:] = np.array(img_pil)

    def draw_highlight(self, img):
        x, y = self.pos
        w, h = self.size

        # Рисуем кнопку с эффектом нажатия
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['pressed_color'], cv2.FILLED)

        # Конвертируем изображение в формат PIL
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Рисуем текст на кнопке
        text_size = draw.textsize(self.text, font=self.font)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h - text_size[1]) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_pressed_color']))

        # Обратно конвертируем изображение в формат OpenCV
        img[:] = np.array(img_pil)

    def is_hovered(self, finger_tip):
        x, y = self.pos
        w, h = self.size
        if x < finger_tip[0] < x + w and y < finger_tip[1] < y + h:
            return True
        return False

    def is_pressed(self, finger_tip_index, finger_tip_middle):
        """
        Проверяет, нажата ли кнопка.

        Нажатие определяется, если указательный палец находится над кнопкой
        и средний палец находится на расстоянии менее порогового значения.

        :param finger_tip_index: Координаты кончика указательного пальца [x, y]
        :param finger_tip_middle: Координаты кончика среднего пальца [x, y]
        :return: True, если кнопка считается нажатой, иначе False
        """
        if self.is_hovered(finger_tip_index):
            distance = np.linalg.norm(np.array(finger_tip_index) - np.array(finger_tip_middle))
            if distance < 40:  # Пороговое значение расстояния между пальцами
                return True
        return False
