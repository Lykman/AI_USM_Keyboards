import cv2
import numpy as np
import pygame
from pynput.keyboard import Controller
from modules.hand_detector import HandDetector
from modules.keyboard import Keyboard
import os
from PIL import ImageFont, ImageDraw, Image

# Initialize the keyboard controller
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
hand_detector = HandDetector(detectionCon=0.8, maxHands=1)

# Initial settings
current_theme = 'theme1'
current_language = 'EN'
virtual_keyboard = Keyboard(language=current_language, theme=current_theme)

# Camera initialization
camera_index = 0  # Your camera index
cap = cv2.VideoCapture(camera_index)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

if not cap.isOpened():
    print(f"Error: Could not open camera with index {camera_index}.")
    exit()

# Variable to store typed text
typed_text = ''
font_paths = ['assets/fonts/Apple Color Emoji.ttc', 'assets/fonts/Arial.ttf']  # Font paths
font = None
font_size = 40

# Load font
for path in font_paths:
    if os.path.exists(path):
        try:
            font = ImageFont.truetype(path, font_size)
            break
        except Exception as e:
            print(f"Warning: Cannot load font '{path}'. {e}")

if not font:
    print("Error: No valid font file found. Exiting.")
    exit()

# Load logo
logo_path = 'assets/icons/AI_USM_logo.png'
if os.path.exists(logo_path):
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    logo = cv2.cvtColor(logo, cv2.COLOR_BGRA2RGBA)
    logo_height, logo_width = logo.shape[:2]
else:
    print(f"Warning: Logo file '{logo_path}' not found.")
    logo = None

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame from camera.")
        break

    img = cv2.flip(img, 1)  # Mirror the image

    # Display logo if available
    if logo is not None:
        x_offset = 10
        y_offset = 10
        y1, y2 = y_offset, y_offset + logo_height
        x1, x2 = x_offset, x_offset + logo_width

        # Ensure logo fits within the image boundaries
        if y2 <= img.shape[0] and x2 <= img.shape[1]:
            # Handle transparency
            alpha_s = logo[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s

            for c in range(0, 3):
                img[y1:y2, x1:x2, c] = (alpha_s * logo[:, :, c] +
                                        alpha_l * img[y1:y2, x1:x2, c])

    # Hand detection
    hands, img = hand_detector.findHands(img, draw=True)  # Enable hand skeleton drawing

    # Convert image to PIL format for text rendering
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)

    # Draw virtual keyboard
    virtual_keyboard.draw(img)

    # Display typed text at the top of the screen
    text_position = (50, 50)
    draw.text(text_position, typed_text, font=font, fill=(0, 0, 0))

    # Convert image back to OpenCV format
    img = np.array(img_pil)

    if hands:
        lmList = hands[0]['lmList']

        finger_tip_index = lmList[8]   # Index finger tip
        finger_tip_middle = lmList[12]  # Middle finger tip

        # Check for interactions with UI buttons
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
                        button.draw_highlight(img)  # Highlight button on press
                        if not key_pressed:
                            typed_text += button.text
                            # Simulate key press in the system
                            keyboard_controller.press(button.text)
                            keyboard_controller.release(button.text)
                            if sound_enabled:
                                key_sound.play()
                            key_pressed = True
                            cv2.waitKey(300)
                    else:
                        button.draw_hover(img)  # Hover highlight
                else:
                    button.draw(img)  # Normal button drawing
    else:
        # Draw buttons if no hands are detected
        virtual_keyboard.draw(img)

    cv2.imshow("AI USM Keyboards", img)
    
    # Wait to control frame rate
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
