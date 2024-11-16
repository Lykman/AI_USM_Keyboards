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

        # Путь к шрифту
        self.font_path = 'assets/fonts/Arial.ttf'  # Убедитесь, что этот файл существует

        if not os.path.exists(self.font_path):
            print(f"Error: Font file '{self.font_path}' not found.")
            exit()

        self.font_size = 24  # Размер шрифта
        try:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
        except Exception as e:
            print(f"Error: Cannot load font '{self.font_path}'. {e}")
            exit()

    def draw(self, img):
        x, y = self.pos
        w, h = self.size

        # Создаем прозрачный оверлей
        overlay = img.copy()
        alpha = 0.0  # Прозрачность

        # Рисуем прозрачный прямоугольник (кнопку) с закругленными углами
        cv2.rectangle(overlay, (x, y), (x + w, y + h), self.theme['button_color'], -1, cv2.LINE_AA)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Рисуем рамку с закругленными углами
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2, cv2.LINE_AA)

        # Конвертируем изображение в формат PIL для рисования текста
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Рассчитываем размер текста
        text_width, text_height = self.font.getsize(self.text)

        # Рисуем текст на кнопке
        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_color']))

        # Обратно конвертируем изображение в формат OpenCV
        img[:] = np.array(img_pil)

    def draw_hover(self, img):
        x, y = self.pos
        w, h = self.size

        # Создаем прозрачный оверлей
        overlay = img.copy()
        alpha = 0.1  # Прозрачность при наведении

        # Рисуем прозрачный прямоугольник (кнопку)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), self.theme['hover_color'], -1, cv2.LINE_AA)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Рисуем рамку
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2, cv2.LINE_AA)

        # Конвертируем изображение в формат PIL для рисования текста
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Рассчитываем размер текста
        text_width, text_height = self.font.getsize(self.text)

        # Рисуем текст на кнопке
        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_hover_color']))

        # Обратно конвертируем изображение в формат OpenCV
        img[:] = np.array(img_pil)

    def draw_highlight(self, img):
        x, y = self.pos
        w, h = self.size

        # Создаем прозрачный оверлей
        overlay = img.copy()
        alpha = 0.2  # Прозрачность при нажатии

        # Рисуем прозрачный прямоугольник (кнопку)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), self.theme['pressed_color'], -1, cv2.LINE_AA)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Рисуем рамку
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2, cv2.LINE_AA)

        # Конвертируем изображение в формат PIL для рисования текста
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Рассчитываем размер текста
        text_width, text_height = self.font.getsize(self.text)

        # Рисуем текст на кнопке
        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

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
        if self.is_hovered(finger_tip_index):
            distance = np.linalg.norm(np.array(finger_tip_index) - np.array(finger_tip_middle))
            if distance < 40:  # Пороговое значение для определения нажатия
                return True
        return False
