import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os

class Button:
    def __init__(self, pos, size, text, theme):
        self.pos = pos              # Button position [x, y]
        self.size = size            # Button size [width, height]
        self.text = text            # Text on the button
        self.theme = theme          # Button theme

        # Path to the font supporting Cyrillic
        self.font_path = 'assets/fonts/Arial.ttf'  # Ensure this file exists

        if not os.path.exists(self.font_path):
            print(f"Error: Font file '{self.font_path}' not found.")
            exit()

        self.font_size = 30  # Font size
        try:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
        except Exception as e:
            print(f"Error: Cannot load font '{self.font_path}'. {e}")
            exit()

    def draw(self, img):
        x, y = self.pos
        w, h = self.size

        # Create transparent overlay
        overlay = img.copy()
        alpha = 0.0  # Transparency

        # Draw transparent rectangle (button)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), self.theme['button_color'], -1)

        # Blend overlay with the image
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Draw border
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2)

        # Convert image to PIL format for text drawing
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Calculate text size
        if hasattr(draw, 'textbbox'):
            text_bbox = draw.textbbox((0, 0), self.text, font=self.font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        else:
            text_width, text_height = self.font.getsize(self.text)

        # Draw text on the button
        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_color']))

        # Convert back to OpenCV image
        img[:] = np.array(img_pil)

    def draw_hover(self, img):
        x, y = self.pos
        w, h = self.size

        # Create transparent overlay
        overlay = img.copy()
        alpha = 0.1  # Transparency on hover

        # Draw transparent rectangle (button)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), self.theme['hover_color'], -1)

        # Blend overlay with the image
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Draw border
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2)

        # Convert image to PIL format for text drawing
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Calculate text size
        if hasattr(draw, 'textbbox'):
            text_bbox = draw.textbbox((0, 0), self.text, font=self.font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        else:
            text_width, text_height = self.font.getsize(self.text)

        # Draw text on the button
        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

        draw.text((text_x, text_y), self.text, font=self.font, fill=tuple(self.theme['text_hover_color']))

        # Convert back to OpenCV image
        img[:] = np.array(img_pil)

    def draw_highlight(self, img):
        x, y = self.pos
        w, h = self.size

        # Create transparent overlay
        overlay = img.copy()
        alpha = 0.2  # Transparency on press

        # Draw transparent rectangle (button)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), self.theme['pressed_color'], -1)

        # Blend overlay with the image
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Draw border
        cv2.rectangle(img, (x, y), (x + w, y + h), self.theme['border_color'], 2)

        # Convert image to PIL format for text drawing
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        # Calculate text size
        if hasattr(draw, 'textbbox'):
            text_bbox = draw.textbbox((0, 0), self.text, font=self.font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        else:
            text_width, text_height = self.font.getsize(self.text)

        # Draw text on the button
        text_x = x + (w - text_width) // 2
        text_y = y + (h - text_height) // 2

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
            if distance < 40:  # Threshold for determining a press
                return True
        return False
