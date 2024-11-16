import json
import cv2
from modules.button import Button

class Keyboard:
    def __init__(self, language='EN', theme='theme1'):
        self.language = language
        self.theme_name = theme
        self.theme = self.load_theme(theme)
        self.layout = self.load_layout(language)
        self.buttons = self.create_buttons()
        self.create_interface_buttons()

    def load_layout(self, language):
        with open(f'assets/layouts/{language.lower()}_layout.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def load_theme(self, theme_name):
        with open(f'assets/themes/{theme_name}.json', 'r') as file:
            return json.load(file)

    def create_buttons(self):
        buttons = []
        for key_data in self.layout:
            button = Button(pos=key_data['pos'], size=key_data['size'], text=key_data['text'], theme=self.theme)
            buttons.append(button)
        return buttons

    def create_interface_buttons(self):
        # Кнопка смены темы
        self.theme_button = Button(pos=[50, 50], size=[80, 80], text='Theme', theme=self.theme)
        # Кнопка смены языка
        self.language_button = Button(pos=[150, 50], size=[80, 80], text='Lang', theme=self.theme)

    def draw_background(self, img):
        # Рисуем полупрозрачный фон
        overlay = img.copy()
        alpha = 0.5  # Коэффициент прозрачности
        background_color = self.theme['background_color']
        overlay[:] = background_color
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    def draw(self, img):
        # Рисуем фон
        self.draw_background(img)
        # Рисуем кнопки клавиатуры
        for button in self.buttons:
            button.draw(img)
        # Рисуем интерфейсные кнопки
        self.theme_button.draw(img)
        self.language_button.draw(img)
