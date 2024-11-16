# modules/gesture_control.py
from GestureRecognition import GestureRecognizer

class GestureControl:
    def __init__(self):
        self.recognizer = GestureRecognizer()

    def detect_gesture(self, landmarks):
        gesture = self.recognizer.recognize(landmarks)
        return gesture
