import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, detectionCon=0.8, maxHands=1):
        self.mode = False
        self.maxHands = maxHands
        self.detectionCon = detectionCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                myHand = {}
                lmList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py = int(lm.x * w), int(lm.y * h)
                    lmList.append([px, py])
                myHand["lmList"] = lmList
                allHands.append(myHand)

                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return allHands, img
