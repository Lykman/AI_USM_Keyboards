import cv2
import numpy as np
import pygame
from pynput.keyboard import Controller
from modules.hand_detector import HandDetector
from modules.keyboard import Keyboard
import os
from PIL import ImageFont, ImageDraw, Image

# Инициализация контроллера клавиатуры
keyboard_controller = Controller()

# Инициализация pygame для работы со звуком
pygame.mixer.init()

# Загрузка звука нажатия клавиш
sound_path = 'assets/sounds/key_press.wav'
if os.path.exists(sound_path):
    key_sound = pygame.mixer.Sound(sound_path)
    sound_enabled = True
else:
    print(f"Warning: Sound file '{sound_path}' not found. Sound will be disabled.")
    sound_enabled = False

# Инициализация детектора рук
hand_detector = HandDetector(detectionCon=0.8)

# Начальные настройки
current_theme = 'theme1'
current_language = 'EN'
virtual_keyboard = Keyboard(language=current_language, theme=current_theme)

# Инициализация камеры
camera_index = 0  # Используйте индекс вашей камеры
cap = cv2.VideoCapture(camera_index)
cap.set(3, 1280)  # Ширина
cap.set(4, 720)   # Высота

if not cap.isOpened():
    print(f"Error: Could not open camera with index {camera_index}.")
    exit()

# Переменная для хранения введённого текста
typed_text = ''
font_path = 'assets/fonts/arial.ttf'  # Путь к шрифту

if not os.path.exists(font_path):
    print(f"Error: Font file '{font_path}' not found.")
    exit()

font_size = 40
font = ImageFont.truetype(font_path, font_size)

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame from camera.")
        break

    img = cv2.flip(img, 1)  # Отражение изображения

    # Конвертируем изображение в формат PIL для отображения текста
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)

    # Обнаружение рук
    hands, img = hand_detector.findHands(img, draw=False)  # Отключаем рисование скелета руки
    lmList = hands[0]['lmList'] if hands else []

    # Рисуем виртуальную клавиатуру
    virtual_keyboard.draw(img)

    # Отображение введённого текста в верхней части экрана
    text_position = (50, 50)
    draw.text(text_position, typed_text, font=font, fill=(0, 0, 0))

    # Обратно конвертируем изображение в формат OpenCV
    img = np.array(img_pil)

    if lmList:
        finger_tip_index = lmList[8]   # Кончик указательного пальца
        finger_tip_middle = lmList[12]  # Кончик среднего пальца

        # Проверка нажатия на интерфейсные кнопки
        if virtual_keyboard.theme_button.is_hovered(finger_tip_index):
            if virtual_keyboard.theme_button.is_pressed(finger_tip_index, finger_tip_middle):
                # Смена темы
                themes = ['theme1', 'theme2', 'theme3']
                current_index = themes.index(current_theme)
                current_theme = themes[(current_index + 1) % len(themes)]
                virtual_keyboard = Keyboard(language=current_language, theme=current_theme)
                cv2.waitKey(300)
            else:
                virtual_keyboard.theme_button.draw_hover(img)
        elif virtual_keyboard.language_button.is_hovered(finger_tip_index):
            if virtual_keyboard.language_button.is_pressed(finger_tip_index, finger_tip_middle):
                # Смена языка
                current_language = 'RU' if current_language == 'EN' else 'EN'
                virtual_keyboard = Keyboard(language=current_language, theme=current_theme)
                cv2.waitKey(300)
            else:
                virtual_keyboard.language_button.draw_hover(img)
        else:
            key_pressed = False
            for button in virtual_keyboard.buttons:
                if button.is_hovered(finger_tip_index):
                    if button.is_pressed(finger_tip_index, finger_tip_middle):
                        button.draw_highlight(img)  # Подсветка кнопки при нажатии
                        if not key_pressed:
                            typed_text += button.text
                            # Отправляем нажатие клавиши в систему
                            keyboard_controller.press(button.text)
                            keyboard_controller.release(button.text)
                            if sound_enabled:
                                key_sound.play()
                            key_pressed = True
                            cv2.waitKey(300)
                    else:
                        button.draw_hover(img)  # Подсветка кнопки при наведении
                else:
                    button.draw(img)  # Обычная отрисовка кнопки
    else:
        # Если нет рук в кадре, просто рисуем кнопки
        virtual_keyboard.draw(img)

    cv2.imshow("AI USM Keyboards", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
