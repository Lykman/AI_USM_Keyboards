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
        theme_path = f'assets/themes/{theme_name}.json'
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
                "border_color": [100, 100, 255],
                "background_color": [50, 50, 50]
            }
        return theme

    def load_layout(self, language):
        layout_path = f'assets/layouts/{language.lower()}_layout.json'
        if os.path.exists(layout_path):
            with open(layout_path, 'r', encoding='utf-8') as f:
                layout = json.load(f)
        else:
            print(f"Warning: Layout file '{layout_path}' not found.")
            layout = []
        return layout

    def create_buttons(self):
        self.buttons = []
        # Настройка размера и позиции кнопок
        button_width = 60
        button_height = 60
        start_x = 50
        start_y = 400  # Положение клавиатуры по вертикали
        gap_x = 10     # Увеличиваем расстояние между кнопками
        gap_y = 15

        for i, row in enumerate(self.layout):
            for j, key in enumerate(row):
                x = start_x + j * (button_width + gap_x)
                y = start_y + i * (button_height + gap_y)
                button = Button(
                    pos=[x, y],
                    size=[button_width, button_height],
                    text=key,
                    theme=self.theme
                )
                self.buttons.append(button)

    def create_interface_buttons(self):
        # Создание кнопок интерфейса (смена темы и языка)
        screen_width = 1280
        self.theme_button = Button(
            pos=[screen_width - 220, 50],
            size=[100, 50],
            text='Theme',
            theme=self.theme
        )
        self.language_button = Button(
            pos=[screen_width - 110, 50],
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
