# modules/button.py
import cv2

class Button:
    def __init__(self, pos, size, text, theme):
        self.pos = pos
        self.size = size
        self.text = text
        self.theme = theme

    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        # Рисуем кнопку
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['button_color'], cv2.FILLED)
        # Рисуем текст
        font_scale = 2
        font_thickness = 2
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_PLAIN, font_scale, font_thickness)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, font_scale, self.theme['text_color'], font_thickness)

    def is_pressed(self, finger_tip):
        x, y = self.pos
        w, h = self.size
        if x < finger_tip[0] < x + w and y < finger_tip[1] < y + h:
            return True
        return False
import cv2

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
        font_scale = 2
        font_thickness = 2
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_PLAIN, font_scale, font_thickness)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, font_scale, self.theme['text_color'], font_thickness)

    def draw_hover(self, img):
        x, y = self.pos
        w, h = self.size
        # Рисуем кнопку с эффектом наведения
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['hover_color'], cv2.FILLED)
        # Рисуем текст
        font_scale = 2
        font_thickness = 2
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_PLAIN, font_scale, font_thickness)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, font_scale, self.theme['text_hover_color'], font_thickness)

    def draw_highlight(self, img):
        x, y = self.pos
        w, h = self.size
        # Рисуем кнопку с эффектом нажатия
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['pressed_color'], cv2.FILLED)
        # Рисуем текст
        font_scale = 2
        font_thickness = 2
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_PLAIN, font_scale, font_thickness)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, font_scale, self.theme['text_pressed_color'], font_thickness)

    def is_pressed(self, finger_tip_index, finger_tip_middle):
        if self.is_hovered(finger_tip_index):
            distance = ((finger_tip_index[0] - finger_tip_middle[0]) ** 2 + (finger_tip_index[1] - finger_tip_middle[1]) ** 2) ** 0.5
            if distance < 40:  # Пороговое значение
                return True
        return False

    def is_hovered(self, finger_tip):
        x, y = self.pos
        w, h = self.size
        if x < finger_tip[0] < x + w and y < finger_tip[1] < y + h:
            return True
        return False
