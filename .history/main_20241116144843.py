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
hand_detector = HandDetector(detectionCon=0.8, maxHands=1)

# Начальные настройки
current_theme = 'theme1'
current_language = 'EN'
virtual_keyboard = Keyboard(language=current_language, theme=current_theme)

# Инициализация камеры с уменьшенным разрешением для повышения производительности
camera_index = 0  # Используйте индекс вашей камеры
cap = cv2.VideoCapture(camera_index)
cap.set(3, 640)  # Ширина
cap.set(4, 480)  # Высота

if not cap.isOpened():
    print(f"Error: Could not open camera with index {camera_index}.")
    exit()

# Переменная для хранения введённого текста
typed_text = ''
font_path = 'assets/fonts/Apple Color Emoji.ttc'  # Путь к шрифту с поддержкой эмодзи

if not os.path.exists(font_path):
    print(f"Error: Font file '{font_path}' not found.")
    exit()

font_size = 40
try:
    font = ImageFont.truetype(font_path, font_size)
except Exception as e:
    print(f"Error: Cannot load font '{font_path}'. {e}")
    exit()

# Загрузка логотипа
logo_path = 'assets/icons/AI_USM_logo.png'
if os.path.exists(logo_path):
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    logo_height, logo_width = logo.shape[:2]
else:
    print(f"Warning: Logo file '{logo_path}' not found.")
    logo = None

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame from camera.")
        break

    img = cv2.flip(img, 1)  # Отражение изображения

    # Отображение логотипа
    if logo is not None:
        # Определяем позицию логотипа
        x_offset = 10
        y_offset = 10
        y1, y2 = y_offset, y_offset + logo_height
        x1, x2 = x_offset, x_offset + logo_width

        # Проверяем размеры
        if y2 <= img.shape[0] and x2 <= img.shape[1]:
            # Обработка прозрачности
            alpha_s = logo[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s

            for c in range(0, 3):
                img[y1:y2, x1:x2, c] = (alpha_s * logo[:, :, c] +
                                        alpha_l * img[y1:y2, x1:x2, c])

    # Обнаружение рук
    hands, img = hand_detector.findHands(img, draw=True)  # Включаем рисование скелета руки

    # Конвертируем изображение в формат PIL для отображения текста
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    # Отображение введённого текста в верхней части экрана
    text_position = (50, 100)
    draw.text(text_position, typed_text, font=font, fill=(0, 0, 0))

    # Обратно конвертируем изображение в формат OpenCV
    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # Рисуем виртуальную клавиатуру
    virtual_keyboard.draw(img)

    if hands:
        lmList = hands[0]['lmList']

        finger_tip_index = lmList[8][:2]   # Кончик указательного пальца
        finger_tip_middle = lmList[12][:2]  # Кончик среднего пальца

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
                            if button.text == 'Space':
                                typed_text += ' '
                                keyboard_controller.press(' ')
                                keyboard_controller.release(' ')
                            elif button.text == 'Delete':
                                typed_text = typed_text[:-1]
                                keyboard_controller.press('\b')
                                keyboard_controller.release('\b')
                            elif button.text == 'Enter':
                                typed_text += '\n'
                                keyboard_controller.press('\n')
                                keyboard_controller.release('\n')
                            elif button.text == 'Shift':
                                # Здесь можно реализовать переключение регистра букв
                                pass
                            else:
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
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
