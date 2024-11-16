# main.py
import cv2
from modules.hand_detector import HandDetector
from modules.keyboard import Keyboard
from modules.gesture_control import GestureControl
from pynput.keyboard import Controller
import numpy as np

# Инициализация
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

hand_detector = HandDetector(detectionCon=0.8)
gesture_control = GestureControl()
keyboard_controller = Controller()

# Начальные настройки
current_theme = 'theme1'
current_language = 'EN'
virtual_keyboard = Keyboard(language=current_language, theme=current_theme)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = hand_detector.findHands(img)
    lmList = hands[0]['lmList'] if hands else []

    # Рисуем виртуальную клавиатуру
    virtual_keyboard.draw(img)

    if lmList:
        gesture = gesture_control.detect_gesture(lmList)

        if gesture == 'OPEN_PALM':
            # Переключение языка
            current_language = 'RU' if current_language == 'EN' else 'EN'
            virtual_keyboard = Keyboard(language=current_language, theme=current_theme)
        elif gesture == 'FIST':
            # Переключение темы
            current_theme = 'theme2' if current_theme == 'theme1' else 'theme3' if current_theme == 'theme2' else 'theme1'
            virtual_keyboard = Keyboard(language=current_language, theme=current_theme)
        elif gesture == 'POINT_UP':
            # Удаление символа
            keyboard_controller.press('\b')
            keyboard_controller.release('\b')
        else:
            # Проверка нажатия на кнопки
            for button in virtual_keyboard.buttons:
                if button.is_pressed(lmList[8]):  # Индексный палец
                    keyboard_controller.press(button.text)
                    keyboard_controller.release(button.text)
                    # Добавьте задержку, чтобы избежать повторного срабатывания
                    cv2.waitKey(300)

    cv2.imshow("AI USM Keyboards", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
