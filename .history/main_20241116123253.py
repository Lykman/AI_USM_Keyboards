import cv2
import numpy as np
import pygame
import argparse
from pynput.keyboard import Controller
from modules import HandDetector, GestureControl, Keyboard

# Парсер аргументов командной строки для выбора камеры
parser = argparse.ArgumentParser(description='AI USM Keyboards')
parser.add_argument('--camera', type=int, default=0, help='Camera device index')
args = parser.parse_args()

# Инициализация камеры
cap = cv2.VideoCapture(args.camera)
cap.set(3, 1280)
cap.set(4, 720)

if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

# Инициализация детектора рук
hand_detector = HandDetector(detectionCon=0.8)
# Инициализация управления жестами
gesture_control = GestureControl()
# Инициализация контроллера клавиатуры
keyboard_controller = Controller()

# Инициализация pygame для работы со звуком
pygame.mixer.init()
# Загрузка звука нажатия клавиш
key_sound = pygame.mixer.Sound('assets/sounds/key_press.wav')

# Загрузка логотипа
logo = cv2.imread('assets/icons/AI_USM_logo.png', cv2.IMREAD_UNCHANGED)
logo_height, logo_width = 100, 100
logo = cv2.resize(logo, (logo_width, logo_height))

# Начальные настройки
current_theme = 'theme1'
current_language = 'EN'
virtual_keyboard = Keyboard(language=current_language, theme=current_theme)

def overlay_logo(img, logo):
    x_offset = img.shape[1] - logo.shape[1] - 10  # 10 пикселей от правого края
    y_offset = 10  # 10 пикселей от верхнего края

    y1, y2 = y_offset, y_offset + logo.shape[0]
    x1, x2 = x_offset, x_offset + logo.shape[1]

    if logo.shape[2] == 4:
        # PNG с альфа-каналом
        alpha_logo = logo[:, :, 3] / 255.0
        alpha_img = 1.0 - alpha_logo

        for c in range(0, 3):
            img[y1:y2, x1:x2, c] = (alpha_logo * logo[:, :, c] +
                                    alpha_img * img[y1:y2, x1:x2, c])
    else:
        img[y1:y2, x1:x2] = logo

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame from camera.")
        break

    img = cv2.flip(img, 1)  # Отражение изображения
    hands, img = hand_detector.findHands(img)
    lmList = hands[0]['lmList'] if hands else []

    # Рисуем виртуальную клавиатуру
    virtual_keyboard.draw(img)

    # Наложение логотипа
    overlay_logo(img, logo)

    if lmList:
        finger_tip_index = lmList[8]   # Кончик указательного пальца
        finger_tip_middle = lmList[12]  # Кончик среднего пальца

        # Проверка нажатия на интерфейсные кнопки
        if virtual_keyboard.theme_button.is_pressed(finger_tip_index):
            # Смена темы
            themes = ['theme1', 'theme2', 'theme3']
            current_index = themes.index(current_theme)
            current_theme = themes[(current_index + 1) % len(themes)]
            virtual_keyboard = Keyboard(language=current_language, theme=current_theme)
            cv2.waitKey(300)

        elif virtual_keyboard.language_button.is_pressed(finger_tip_index):
            # Смена языка
            current_language = 'RU' if current_language == 'EN' else 'EN'
            virtual_keyboard = Keyboard(language=current_language, theme=current_theme)
            cv2.waitKey(300)

        else:
            # Логика нажатия клавиш
            key_pressed = False
            for button in virtual_keyboard.buttons:
                if button.is_hovered(finger_tip_index):
                    # Проверяем, находится ли средний палец рядом с указательным
                    distance = np.linalg.norm(np.array(finger_tip_index) - np.array(finger_tip_middle))
                    if distance < 40:  # Пороговое значение, можно настроить
                        button.draw_highlight(img)  # Подсветка кнопки при нажатии
                        if not key_pressed:
                            keyboard_controller.press(button.text)
                            keyboard_controller.release(button.text)
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
