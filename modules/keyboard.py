import json
from modules.button import Button
import os

class Keyboard:
    def __init__(self, language='EN', theme='theme1', frame_width=1280, frame_height=720):
        self.language = language
        self.theme_name = theme
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.theme = self.load_theme(theme)
        self.layout = self.load_layout(language)
        self.buttons = []
        self.font_path = 'assets/fonts/Arial.ttf'  # Путь к шрифту Arial
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
        button_height = int(self.frame_height * 0.07)  # Уменьшили до 7%
        gap_x = int(self.frame_width * 0.004)         # 0.4% от ширины кадра
        gap_y = int(self.frame_height * 0.004)        # 0.4% от высоты кадра
        start_y = int(self.frame_height * 0.65)       # Начинаем с 65% высоты экрана

        for i, row in enumerate(self.layout):
            num_keys = len(row)
            total_gap = gap_x * (num_keys - 1)
            total_width = int(self.frame_width * 0.8)  # 80% от ширины кадра
            button_width = (total_width - total_gap) // num_keys
            start_x = int((self.frame_width - (button_width * num_keys + total_gap)) / 2)
            font_size = max(int(button_height * 0.35), 14)  # Уменьшили до 35%

            for j, key in enumerate(row):
                x = int(start_x + j * (button_width + gap_x))
                y = int(start_y + i * (button_height + gap_y))
                button = Button(
                    pos=[x, y],
                    size=[button_width, button_height],
                    text=key,
                    theme=self.theme,
                    font_path=self.font_path,
                    font_size=font_size,
                    opacity=0.6  # Прозрачность кнопок
                )
                self.buttons.append(button)

    def create_interface_buttons(self):
        # Создание кнопок интерфейса (смена темы и языка)
        button_width = int(self.frame_width * 0.08)  # Уменьшили до 8%
        button_height = int(self.frame_height * 0.05)  # Уменьшили до 5%
        font_size = max(int(button_height * 0.4), 12)  # Минимальный размер шрифта 12

        # Размещаем кнопки в верхней части экрана, с правой стороны
        padding = 10
        self.theme_button = Button(
            pos=[self.frame_width - 2 * button_width - 2 * padding, padding],
            size=[button_width, button_height],
            text='T',
            theme=self.theme,
            font_path=self.font_path,
            font_size=font_size,
            opacity=0.6
        )
        self.language_button = Button(
            pos=[self.frame_width - button_width - padding, padding],
            size=[button_width, button_height],
            text='L',
            theme=self.theme,
            font_path=self.font_path,
            font_size=font_size,
            opacity=0.6
        )

    def update_frame_size(self, frame_width, frame_height):
        if frame_width != self.frame_width or frame_height != self.frame_height:
            self.frame_width = frame_width
            self.frame_height = frame_height
            self.theme = self.load_theme(self.theme_name)
            self.layout = self.load_layout(self.language)
            self.create_buttons()
            self.create_interface_buttons()

    def draw(self, img):
        # Рисуем все кнопки клавиатуры
        for button in self.buttons:
            button.draw(img)
        # Рисуем кнопки интерфейса
        self.theme_button.draw(img)
        self.language_button.draw(img)
