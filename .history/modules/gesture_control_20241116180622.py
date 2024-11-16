import json
import math
import os

class GestureControl:
    def __init__(self):
        settings_path = 'settings.json'
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as file:
                settings = json.load(file)
            self.sensitivity = settings.get('gesture_sensitivity', 0.8)
        else:
            self.sensitivity = 0.8  # Значение по умолчанию

    def detect_gesture(self, lmList):
        if not lmList:
            return None

        # Определяем открытые пальцы
        fingers = []

        # Большой палец
        if lmList[4][0] > lmList[3][0]:
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
        else:
            # Проверка жеста PINCH (схлопывание большого и указательного пальцев)
            thumb_tip = lmList[4]
            index_tip = lmList[8]
            distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])
            # Пороговое значение для определения жеста PINCH, можно настроить
            if distance < 40:  # Значение может потребовать настройки
                return 'PINCH'

        return 'UNKNOWN'
