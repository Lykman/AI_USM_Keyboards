import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os

class Button:
    def __init__(self, pos, size, text, theme, font_path, font_size, opacity=0.6):
        self.pos = [int(pos[0]), int(pos[1])]      # Позиция кнопки [x, y]
        self.size = [int(size[0]), int(size[1])]   # Размер кнопки [width, height]
        self.text = text                            # Текст на кнопке
        self.theme = theme                          # Тема оформления кнопки
        self.font_path = font_path
        self.font_size = font_size
        self.opacity = opacity                      # Прозрачность кнопки (0.0 - 1.0)

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

        # Цвета
        button_color = np.array(self.theme['button_color'], dtype=np.uint8)
        border_color = np.array(self.theme['border_color'], dtype=np.uint8)

        # Создаем полупрозрачную кнопку
        overlay = img.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), button_color.tolist(), -1)
        cv2.addWeighted(overlay, self.opacity, img, 1 - self.opacity, 0, img)

        # Рисуем границу кнопки
        cv2.rectangle(img, (x, y), (x + w, y + h), border_color.tolist(), 2)

        # Рисуем текст
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw_pil = ImageDraw.Draw(img_pil)
        text = self.text

        try:
            text_bbox = self.font.getbbox(text)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        except AttributeError:
            # Если getbbox недоступен, используем textsize
            text_width, text_height = draw_pil.textsize(text, font=self.font)

        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

        text_color = tuple(int(c) for c in self.theme['text_color'])
        draw_pil.text((text_x, text_y), text, font=self.font, fill=text_color)

        img[:] = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def draw_hover(self, img):
        x, y = self.pos
        w, h = self.size

        # Цвета при наведении
        hover_color = np.array(self.theme['hover_color'], dtype=np.uint8)
        border_color = np.array(self.theme['border_color'], dtype=np.uint8)

        # Создаем полупрозрачную кнопку
        overlay = img.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), hover_color.tolist(), -1)
        cv2.addWeighted(overlay, self.opacity, img, 1 - self.opacity, 0, img)

        # Рисуем границу кнопки
        cv2.rectangle(img, (x, y), (x + w, y + h), border_color.tolist(), 2)

        # Рисуем текст
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw_pil = ImageDraw.Draw(img_pil)
        text = self.text

        try:
            text_bbox = self.font.getbbox(text)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        except AttributeError:
            # Если getbbox недоступен, используем textsize
            text_width, text_height = draw_pil.textsize(text, font=self.font)

        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

        text_color = tuple(int(c) for c in self.theme['text_hover_color'])
        draw_pil.text((text_x, text_y), text, font=self.font, fill=text_color)

        img[:] = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def draw_highlight(self, img):
        x, y = self.pos
        w, h = self.size

        # Цвета при нажатии
        pressed_color = np.array(self.theme['pressed_color'], dtype=np.uint8)
        border_color = np.array(self.theme['border_color'], dtype=np.uint8)

        # Создаем полупрозрачную кнопку
        overlay = img.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), pressed_color.tolist(), -1)
        cv2.addWeighted(overlay, self.opacity, img, 1 - self.opacity, 0, img)

        # Рисуем границу кнопки
        cv2.rectangle(img, (x, y), (x + w, y + h), border_color.tolist(), 2)

        # Рисуем текст
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2R
