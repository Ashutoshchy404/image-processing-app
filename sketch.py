# sketch.py
import cv2
import numpy as np

def convert_to_sketch(image):
    """Convert an image to pencil sketch effect."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Invert and blur
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (111, 111), 0)
    inverted_blurred = cv2.bitwise_not(blurred)
    
    # Create sketch
    sketch = cv2.divide(gray, inverted_blurred, scale=256.0)
    return sketch