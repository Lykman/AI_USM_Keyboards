# modules/keyboard.py

import json
from modules.button import Button
import os

class Keyboard:
    def __init__(self, language='EN', theme='theme1'):
        self.language = language
        self.theme_name = theme
        self.theme = self.load_theme(theme)
        self.layout = self.load_layout(language)
        self.buttons = []
        self.create_buttons()
        self.create_interface_buttons()

    def load_theme(self, theme_name):
        theme_path = f'themes/{theme_name}.json'
        if os.path.exists(theme_path):
            with open(theme_path, 'r') as f:
                theme = json.load(f)
        else:
            print(f"Warning: Theme file '{theme_path}' not found. Using default theme.")
            theme = {
                "button_color": [255, 255, 255],
                "text_color": [0, 0, 0],
                "hover_color": [200, 200, 200],
                "text_hover_color": [0, 0, 0],
                "pressed_color": [150, 150, 150],
                "text_pressed_color": [0, 0, 0],
                "background_color": [50, 50, 50]
            }
        return theme

    def load_layout(self, language):
        layout_path = f'layouts/{language}.json'
        if os.path.exists(layout_path):
            with open(layout_path, 'r', encoding='utf-8') as f:
                layout = json.load(f)
        else:
            print(f"Warning: Layout file '{layout_path}' not found.")
            layout = []
        return layout

    def create_buttons(self):
        self.buttons = []
        # Настройка размера и позиции кнопок для размещения на экране
        button_width = 50
        button_height = 50
        start_x = 50
        start_y = 400  # Положение клавиатуры по вертикали
        gap = 5

        for i, row in enumerate(self.layout):
            for j, key in enumerate(row):
                x = start_x + j * (button_width + gap)
                y = start_y + i * (button_height + gap)
                button = Button(
                    pos=[x, y],
                    size=[button_width, button_height],
                    text=key,
                    theme=self.theme
                )
                self.buttons.append(button)

    def create_interface_buttons(self):
        # Создание кнопок интерфейса (смена темы и языка)
        self.theme_button = Button(
            pos=[50, 50],
            size=[100, 50],
            text='Theme',
            theme=self.theme
        )
        self.language_button = Button(
            pos=[160, 50],
            size=[100, 50],
            text='Lang',
            theme=self.theme
        )

    def draw(self, img):
        # Рисуем все кнопки клавиатуры
        for button in self.buttons:
            button.draw(img)
        # Рисуем кнопки интерфейса
        self.theme_button.draw(img)
        self.language_button.draw(img)
