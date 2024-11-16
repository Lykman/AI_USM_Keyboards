import cv2
from modules.hand_detector import HandDetector
from modules.keyboard import Keyboard
from modules.gesture_control import GestureControl
from pynput.keyboard import Controller
import numpy as np

# Инициализация
cap = cv2.VideoCapture(0)
hand_detector = HandDetector(detectionCon=0.8)
gesture_control = GestureControl()
keyboard = Controller()

# Начальные настройки
current_theme = 'theme1'
current_language = 'EN'
virtual_keyboard = Keyboard(language=current_language, theme=current_theme)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands = hand_detector.findHands(img)

    # Рисуем виртуальную клавиатуру
    virtual_keyboard.draw(img)

    if hands:
        landmarks = hands[0]['lmList']
        gesture = gesture_control.detect_gesture(landmarks)

        if gesture == 'SWIPE_LEFT':
            # Переключение темы
            current_theme = 'theme2' if current_theme == 'theme1' else 'theme3' if current_theme == 'theme2' else 'theme1'
            virtual_keyboard = Keyboard(language=current_language, theme=current_theme)
        elif gesture == 'OPEN_PALM':
            # Переключение языка
            current_language = 'RU' if current_language == 'EN' else 'EN'
            virtual_keyboard = Keyboard(language=current_language, theme=current_theme)
        elif gesture == 'POINT_DOWN':
            # Удаление символа
            keyboard.press('\b')
            keyboard.release('\b')
        else:
            # Проверка нажатия на кнопки
            for button in virtual_keyboard.buttons:
                if button.is_pressed(landmarks):
                    keyboard.press(button.text)
                    keyboard.release(button.text)

    cv2.imshow("AI USM Keyboards", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
