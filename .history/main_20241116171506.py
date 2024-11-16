import cv2
import numpy as np
import pygame
from pynput.keyboard import Controller
from modules.hand_detector import HandDetector
from modules.keyboard import Keyboard
import os
from PIL import ImageFont, ImageDraw, Image
import time

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
hand_detector = HandDetector(detectionCon=0.8, maxHands=1)  # Ограничение до одной руки

# Начальные настройки
current_theme = 'theme1'
current_language = 'EN'

# Инициализация камеры
camera_index = 0  # Используйте индекс вашей камеры
cap = cv2.VideoCapture(camera_index)

# Установка разрешения камеры для повышения производительности
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Получаем разрешение камеры
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

if not cap.isOpened():
    print(f"Error: Could not open camera with index {camera_index}.")
    exit()

# Переменная для хранения введённого текста
typed_text = ''
font_path = 'assets/fonts/Arial.ttf'  # Путь к шрифту Arial

if not os.path.exists(font_path):
    print(f"Error: Font file '{font_path}' not found.")
    exit()

# Загрузка логотипа
logo_path = 'assets/icons/AI_USM_logo.png'
if os.path.exists(logo_path):
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    if logo is not None:
        # Масштабируем логотип, если он слишком большой
        max_logo_width = int(frame_width * 0.15)  # Логотип не больше 15% ширины экрана
        scaling_factor = max_logo_width / logo.shape[1]
        logo_width = int(logo.shape[1] * scaling_factor)
        logo_height = int(logo.shape[0] * scaling_factor)
        logo = cv2.resize(logo, (logo_width, logo_height), interpolation=cv2.INTER_AREA)
    else:
        print(f"Warning: Could not read logo file '{logo_path}'.")
        logo = None
else:
    print(f"Warning: Logo file '{logo_path}' not found.")
    logo = None

# Инициализируем виртуальную клавиатуру после получения размеров окна
virtual_keyboard = Keyboard(language=current_language, theme=current_theme, frame_width=frame_width, frame_height=frame_height)

# Переменная для отслеживания состояния Shift (Caps Lock)
shift_active = False

# Для ограничения FPS
prev_time = 0
fps = 30  # Желаемый FPS

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame from camera.")
        break

    img = cv2.flip(img, 1)  # Отражение изображения

    # Обновляем размеры кадра (на случай, если размер окна изменился)
    new_frame_height, new_frame_width = img.shape[:2]
    if new_frame_width != frame_width or new_frame_height != frame_height:
        frame_width, frame_height = new_frame_width, new_frame_height
        virtual_keyboard.update_frame_size(frame_width, frame_height)
        # Масштабируем логотип снова, если размеры изменились
        if logo is not None:
            max_logo_width = int(frame_width * 0.15)
            scaling_factor = max_logo_width / logo.shape[1]
            logo_width = int(logo.shape[1] * scaling_factor)
            logo_height = int(logo.shape[0] * scaling_factor)
            logo = cv2.resize(logo, (logo_width, logo_height), interpolation=cv2.INTER_AREA)

    # Отображение логотипа
    if logo is not None:
        # Определяем позицию логотипа (верхний левый угол с отступом 10 пикселей)
        x_offset = 10
        y_offset = 10
        y1, y2 = y_offset, y_offset + logo_height
        x1, x2 = x_offset, x_offset + logo_width

        # Проверяем размеры
        if y2 <= img.shape[0] and x2 <= img.shape[1]:
            # Обработка прозрачности
            if logo.shape[2] == 4:
                alpha_s = logo[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s

                for c in range(0, 3):
                    img[y1:y2, x1:x2, c] = (alpha_s * logo[:, :, c] +
                                            alpha_l * img[y1:y2, x1:x2, c])
            else:
                img[y1:y2, x1:x2] = logo

    # Обнаружение рук
    hands, img = hand_detector.findHands(img, draw=True)  # Включаем рисование скелета руки

    # Конвертируем изображение в формат PIL для отображения текста
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw_pil = ImageDraw.Draw(img_pil)

    # Отображение введённого текста в верхней части экрана
    font_size = max(int(frame_height * 0.04), 20)  # Уменьшили размер шрифта до 4% высоты экрана
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Error: Cannot load font '{font_path}'. {e}")
        exit()
    text_position = (int(frame_width * 0.05), int(frame_height * 0.05))
    
    # Добавление фона для текста для улучшения читаемости
    text = typed_text
    text_width, text_height = font.getsize(text)
    background_rect = (
        int(frame_width * 0.05) - 10, 
        int(frame_height * 0.05) - 5,
        int(frame_width * 0.05) + text_width + 10,
        int(frame_height * 0.05) + text_height + 5
    )
    draw_pil.rectangle(background_rect, fill=(0, 0, 0))  # Чёрный фон
    draw_pil.text(text_position, text, font=font, fill=(255, 255, 255))  # Белый текст

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
                print("Theme button pressed")
                # Смена темы
                themes = ['theme1', 'theme2', 'theme3']
                current_index = themes.index(current_theme)
                current_theme = themes[(current_index + 1) % len(themes)]
                virtual_keyboard = Keyboard(language=current_language, theme=current_theme, frame_width=frame_width, frame_height=frame_height)
                cv2.waitKey(300)
            else:
                virtual_keyboard.theme_button.draw_hover(img)
        elif virtual_keyboard.language_button.is_hovered(finger_tip_index):
            if virtual_keyboard.language_button.is_pressed(finger_tip_index, finger_tip_middle):
                print("Language button pressed")
                # Смена языка
                current_language = 'RU' if current_language == 'EN' else 'EN'
                virtual_keyboard = Keyboard(language=current_language, theme=current_theme, frame_width=frame_width, frame_height=frame_height)
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
                            key_text = button.text
                            if key_text == 'Space':
                                typed_text += ' '
                                keyboard_controller.press(' ')
                                keyboard_controller.release(' ')
                            elif key_text == 'Delete':
                                typed_text = typed_text[:-1]
                                keyboard_controller.press('\b')
                                keyboard_controller.release('\b')
                            elif key_text == 'Enter':
                                typed_text += '\n'
                                keyboard_controller.press('\n')
                                keyboard_controller.release('\n')
                            elif key_text == 'Shift':
                                shift_active = not shift_active  # Переключаем состояние Shift
                                print(f"Shift {'ON' if shift_active else 'OFF'}")
                            else:
                                if shift_active:
                                    key_text = key_text.upper()
                                else:
                                    key_text = key_text.lower()
                                typed_text += key_text
                                # Отправляем нажатие клавиши в систему
                                keyboard_controller.press(key_text)
                                keyboard_controller.release(key_text)
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

    # Ограничение FPS для повышения производительности
    curr_time = time.time()
    elapsed_time = curr_time - prev_time
    if elapsed_time < 1.0 / fps:
        time.sleep(1.0 / fps - elapsed_time)
    prev_time = curr_time

    cv2.imshow("AI USM Keyboards", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
