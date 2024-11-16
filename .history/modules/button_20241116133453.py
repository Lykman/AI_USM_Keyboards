# modules/button.py

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os

class Button:
    def __init__(self, pos, size, text, theme):
        self.pos = pos              # Position of the button [x, y]
        self.size = size            # Size of the button [width, height]
        self.text = text            # Text on the button
        self.theme = theme          # Theme dictionary

        # Path to a font that supports Cyrillic characters
        self.font_path = 'assets/fonts/arial.ttf'  # Make sure this font exists
        self.font_size = 30  # Font size
        self.font = ImageFont.truetype(self.font_path, self.font_size)

    def draw(self, img):
        x, y = self.pos
        w, h = self.size

        # Create a transparent overlay
        overlay = img.copy()
        alpha = 0.0  # Transparency factor (0.0 means fully transparent)

        # Draw a transparent rectangle (button)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), self.theme['button_color'], -1)

        # Blend the overlay with the original image
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Draw the border
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2)

        # Convert to PIL Image to draw text
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Draw the text
        text_size = draw.textsize(self.text, font=self.font)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h - text_size[1]) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_color']))

        # Convert back to OpenCV image
        img[:] = np.array(img_pil)

    def draw_hover(self, img):
        x, y = self.pos
        w, h = self.size

        # Create a transparent overlay
        overlay = img.copy()
        alpha = 0.1  # Slightly less transparent

        # Draw a transparent rectangle (button)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), self.theme['hover_color'], -1)

        # Blend the overlay with the original image
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Draw the border
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2)

        # Convert to PIL Image to draw text
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Draw the text
        text_size = draw.textsize(self.text, font=self.font)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h - text_size[1]) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_hover_color']))

        # Convert back to OpenCV image
        img[:] = np.array(img_pil)

    def draw_highlight(self, img):
        x, y = self.pos
        w, h = self.size

        # Create a transparent overlay
        overlay = img.copy()
        alpha = 0.2  # Slightly less transparent

        # Draw a transparent rectangle (button)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), self.theme['pressed_color'], -1)

        # Blend the overlay with the original image
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Draw the border
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2)

        # Convert to PIL Image to draw text
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Draw the text
        text_size = draw.textsize(self.text, font=self.font)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h - text_size[1]) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_pressed_color']))

        # Convert back to OpenCV image
        img[:] = np.array(img_pil)

    def is_hovered(self, finger_tip):
        x, y = self.pos
        w, h = self.size
        if x < finger_tip[0] < x + w and y < finger_tip[1] < y + h:
            return True
        return False

    def is_pressed(self, finger_tip_index, finger_tip_middle):
        if self.is_hovered(finger_tip_index):
            distance = np.linalg.norm(np.array(finger_tip_index) - np.array(finger_tip_middle))
            if distance < 40:  # Threshold for considering a press
                return True
        return False
