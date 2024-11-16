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
        # Используем цвета из текущей темы
        cv2.rectangle(img, self.pos, (x + w, y + h), self.theme['button_color'], cv2.FILLED)
        cv2.putText(img, self.text, (x + 20, y + h - 20), cv2.FONT_HERSHEY_PLAIN, 2, self.theme['text_color'], 2)
