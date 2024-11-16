# modules/button.py
import cv2
import numpy as np

class Button:
    def __init__(self, pos, size, text, theme):
        self.pos = pos  # [x, y]
        self.size = size  # [width, height]
        self.text = text
        self.theme = theme

    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        # Рисуем кнопку
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['button_color'], cv2.FILLED)
        # Рисуем текст
        font_scale = 1.5
        font_thickness = 2
        text_size, _ = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2 - 5  # -5 для выравнивания по центру
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, self.theme['text_color'], font_thickness)

    def draw_hover(self, img):
        x, y = self.pos
        w, h = self.size
        # Рисуем кнопку с эффектом наведения
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['hover_color'], cv2.FILLED)
        # Рисуем текст
        font_scale = 1.5
        font_thickness = 2
        text_size, _ = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2 - 5
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, self.theme['text_hover_color'], font_thickness)

    def draw_highlight(self, img):
        x, y = self.pos
        w, h = self.size
        # Рисуем кнопку с эффектом нажатия
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['pressed_color'], cv2.FILLED)
        # Рисуем текст
        font_scale = 1.5
        font_thickness = 2
        text_size, _ = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2 - 5
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, self.theme['text_pressed_color'], font_thickness)

    def is_hovered(self, finger_tip):
        x, y = self.pos
        w, h = self.size
        if x < finger_tip[0] < x + w and y < finger_tip[1] < y + h:
            return True
        return False

    def is_pressed(self, finger_tip_index, finger_tip_middle):
        if self.is_hovered(finger_tip_index):
            distance = np.linalg.norm(np.array(finger_tip_index) - np.array(finger_tip_middle))
            if distance < 40:  # Пороговое значение, можно настроить
                return True
        return False
