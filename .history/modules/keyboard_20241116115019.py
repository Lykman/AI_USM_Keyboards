# modules/keyboard.py
import json
from modules.button import Button

class Keyboard:
    def __init__(self, language='EN', theme='theme1'):
        self.language = language
        self.theme = self.load_theme(theme)
        self.layout = self.load_layout(language)
        self.buttons = self.create_buttons()

    def load_layout(self, language):
        with open(f'assets/layouts/{language.lower()}_layout.json', 'r') as file:
            return json.load(file)

    def load_theme(self, theme_name):
        with open(f'assets/themes/{theme_name}.json', 'r') as file:
            return json.load(file)

    def create_buttons(self):
        buttons = []
        # Создаем кнопки на основе макета и темы
        for key_data in self.layout:
            button = Button(pos=key_data['pos'], size=key_data['size'], text=key_data['text'], theme=self.theme)
            buttons.append(button)
        return buttons

    def draw(self, img):
        for button in self.buttons:
            button.draw(img)
