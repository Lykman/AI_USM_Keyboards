import math
import json
import os

class GestureControl:
    def __init__(self):
        # Загрузка настроек из settings.json
        settings_path = 'assets/settings.json'
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as file:
                settings = json.load(file)
            self.sensitivity = settings.get('gesture_sensitivity', 0.8)
        else:
            print(f"Warning: Settings file '{settings_path}' not found. Using default sensitivity.")
            self.sensitivity = 0.8

        # Параметры для определения свайпов
        self.previous_hand_position = None
        self.swipe_threshold = 100  # Пороговое значение для свайпа

    def detect_gesture(self, lmList):
        if not lmList:
            return None

        # Определение расстояния между большим и указательным пальцами
        thumb_tip = lmList[4]
        index_tip = lmList[8]
        distance = math.hypot(thumb_tip[0] - index_tip[0], thumb_tip[1] - index_tip[1])

        # Определение жеста "TWO_FINGERS_TOUCH"
        if distance < self.sensitivity * 50:  # Порог можно настроить в settings.json
            return 'TWO_FINGERS_TOUCH'

        # Определение жестов свайпа
        if self.previous_hand_position:
            dx = lmList[0][0] - self.previous_hand_position[0]
            dy = lmList[0][1] - self.previous_hand_position[1]

            if abs(dx) > self.swipe_threshold and abs(dy) < self.swipe_threshold / 2:
                if dx > 0:
                    gesture = 'SWIPE_RIGHT'
                else:
                    gesture = 'SWIPE_LEFT'
                self.previous_hand_position = lmList[0]
                return gesture

        self.previous_hand_position = lmList[0]

        fingers = []

        # Большой палец
        if thumb_tip[0] > lmList[3][0]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Остальные пальцы
        for id in [8, 12, 16, 20]:
            if lmList[id][1] < lmList[id - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Определение жестов
        if fingers == [0, 1, 1, 1, 1]:
            return 'OPEN_PALM'
        elif fingers == [0, 0, 0, 0, 0]:
            return 'FIST'
        elif fingers == [0, 1, 0, 0, 0]:
            return 'POINT_UP'
        elif fingers == [0, 0, 1, 0, 0]:
            return 'MIDDLE_FINGER'
        # Добавьте другие жесты по необходимости

        return 'UNKNOWN'
