import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os

class Button:
    def __init__(self, pos, size, text, theme, font_path, font_size):
        self.pos = pos              # Позиция кнопки [x, y]
        self.size = size            # Размер кнопки [width, height]
        self.text = text            # Текст на кнопке
        self.theme = theme          # Тема оформления кнопки
        self.font_path = font_path
        self.font_size = font_size

        if not os.path.exists(self.font_path):
            print(f"Error: Font file '{self.font_path}' not found.")
            exit()

        try:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
        except Exception as e:
            print(f"Error: Cannot load font '{self.font_path}'. {e}")
            exit()

    def draw(self, img):
        x, y = self.pos
        w, h = self.size

        # Рисуем кнопку
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['button_color'], -1)
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2)

        # Конвертируем изображение в формат PIL для рисования текста
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        # Рассчитываем размер текста
        bbox = self.font.getbbox(self.text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Рисуем текст на кнопке
        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_color']))

        # Обратно конвертируем изображение в формат OpenCV
        img[:] = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def draw_hover(self, img):
        x, y = self.pos
        w, h = self.size

        # Рисуем кнопку с эффектом наведения
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['hover_color'], -1)
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2)

        # Конвертируем изображение в формат PIL для рисования текста
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        # Рассчитываем размер текста
        bbox = self.font.getbbox(self.text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Рисуем текст на кнопке
        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_hover_color']))

        # Обратно конвертируем изображение в формат OpenCV
        img[:] = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def draw_highlight(self, img):
        x, y = self.pos
        w, h = self.size

        # Рисуем кнопку с эффектом нажатия
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['pressed_color'], -1)
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2)

        # Конвертируем изображение в формат PIL для рисования текста
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        # Рассчитываем размер текста
        bbox = self.font.getbbox(self.text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Рисуем текст на кнопке
        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_pressed_color']))

        # Обратно конвертируем изображение в формат OpenCV
        img[:] = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def is_hovered(self, finger_tip):
        x, y = self.pos
        w, h = self.size
        if x <= finger_tip[0] <= x + w and y <= finger_tip[1] <= y + h:
            return True
        return False

    def is_pressed(self, finger_tip_index, finger_tip_middle):
        if self.is_hovered(finger_tip_index):
            distance = np.linalg.norm(np.array(finger_tip_index) - np.array(finger_tip_middle))
            if distance < (self.size[1] * 0.6):  # Пороговое значение для определения нажатия
                return True
        return False
