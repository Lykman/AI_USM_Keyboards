# modules/gesture_control.py
import cv2
import numpy as np

class GestureControl:
    def __init__(self):
        pass

    def detect_gesture(self, lmList):
        if not lmList:
            return None

        fingers = []

        # Thumb
        if lmList[4][0] > lmList[3][0]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
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
