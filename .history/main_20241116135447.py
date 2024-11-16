import cv2
import numpy as np
import pygame
from pynput.keyboard import Controller
from modules.hand_detector import HandDetector
from modules.keyboard import Keyboard
import os
from PIL import ImageFont, ImageDraw, Image

# Initialize keyboard controller
keyboard_controller = Controller()

# Initialize pygame for sound
pygame.mixer.init()

# Load key press sound
sound_path = 'assets/sounds/key_press.wav'
if os.path.exists(sound_path):
    key_sound = pygame.mixer.Sound(sound_path)
    sound_enabled = True
else:
    print(f"Warning: Sound file '{sound_path}' not found. Sound will be disabled.")
    sound_enabled = False

# Initialize hand detector
hand_detector = HandDetector(detectionCon=0.8)

# Initial settings
current_theme = 'theme1'
current_language = 'EN'
virtual_keyboard = Keyboard(language=current_language, theme=current_theme)

# Initialize camera
camera_index = 0  # Use your camera index
cap = cv2.VideoCapture(camera_index)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

if not cap.isOpened():
    print(f"Error: Could not open camera with index {camera_index}.")
    exit()

# Variable to store typed text
typed_text = ''
font_path = 'assets/fonts/arial.ttf'  # Path to the font

if not os.path.exists(font_path):
    print(f"Error: Font file '{font_path}' not found.")
    exit()

font_size = 40
font = ImageFont.truetype(font_path, font_size)

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame from camera.")
        break

    img = cv2.flip(img, 1)  # Mirror image

    # Convert image to PIL format for text drawing
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)

    # Hand detection
    hands, img = hand_detector.findHands(img, draw=False)  # Disable drawing hand landmarks
    lmList = hands[0]['lmList'] if hands else []

    # Draw virtual keyboard
    virtual_keyboard.draw(img)

    # Display typed text at the top of the screen
    text_position = (50, 50)
    draw.text(text_position, typed_text, font=font, fill=(0, 0, 0))

    # Convert back to OpenCV image
    img = np.array(img_pil)

    if lmList:
        finger_tip_index = lmList[8]   # Index finger tip
        finger_tip_middle = lmList[12]  # Middle finger tip

        # Check for presses on interface buttons
        if virtual_keyboard.theme_button.is_hovered(finger_tip_index):
            if virtual_keyboard.theme_button.is_pressed(finger_tip_index, finger_tip_middle):
                # Change theme
                themes = ['theme1', 'theme2', 'theme3']
                current_index = themes.index(current_theme)
                current_theme = themes[(current_index + 1) % len(themes)]
                virtual_keyboard = Keyboard(language=current_language, theme=current_theme)
                cv2.waitKey(300)
            else:
                virtual_keyboard.theme_button.draw_hover(img)
        elif virtual_keyboard.language_button.is_hovered(finger_tip_index):
            if virtual_keyboard.language_button.is_pressed(finger_tip_index, finger_tip_middle):
                # Change language
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
                        button.draw_highlight(img)  # Highlight button when pressed
                        if not key_pressed:
                            typed_text += button.text
                            # Send key press to system
                            keyboard_controller.press(button.text)
                            keyboard_controller.release(button.text)
                            if sound_enabled:
                                key_sound.play()
                            key_pressed = True
                            cv2.waitKey(300)
                    else:
                        button.draw_hover(img)  # Highlight button when hovered
                else:
                    button.draw(img)  # Regular button draw
    else:
        # No hands detected, just draw buttons
        virtual_keyboard.draw(img)

    cv2.imshow("AI USM Keyboards", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
