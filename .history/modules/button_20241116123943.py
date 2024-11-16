# modules/button.py
import cv2
import numpy as np

class Button:
    def __init__(self, pos, size, text, theme):
        self.pos = pos              # Позиция кнопки [x, y]
        self.size = size            # Размер кнопки [width, height]
        self.text = text            # Текст на кнопке
        self.theme = theme          # Тема оформления кнопки

    def draw(self, img):
        x, y = self.pos
        w, h = self.size

        # Рисуем прямоугольник кнопки
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['button_color'], cv2.FILLED)

        # Рисуем текст на кнопке
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_thickness = 2

        text_size, _ = cv2.getTextSize(self.text, font, font_scale, font_thickness)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2 - 5  # -5 для корректного выравнивания по вертикали

        cv2.putText(img, self.text, (text_x, text_y), font, font_scale, self.theme['text_color'], font_thickness)

    def draw_hover(self, img):
        x, y = self.pos
        w, h = self.size

        # Рисуем кнопку с эффектом наведения
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['hover_color'], cv2.FILLED)

        # Рисуем текст на кнопке
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_thickness = 2

        text_size, _ = cv2.getTextSize(self.text, font, font_scale, font_thickness)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2 - 5

        cv2.putText(img, self.text, (text_x, text_y), font, font_scale, self.theme['text_hover_color'], font_thickness)

    def draw_highlight(self, img):
        x, y = self.pos
        w, h = self.size

        # Рисуем кнопку с эффектом нажатия
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['pressed_color'], cv2.FILLED)

        # Рисуем текст на кнопке
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_thickness = 2

        text_size, _ = cv2.getTextSize(self.text, font, font_scale, font_thickness)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2 - 5

        cv2.putText(img, self.text, (text_x, text_y), font, font_scale, self.theme['text_pressed_color'], font_thickness)

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
