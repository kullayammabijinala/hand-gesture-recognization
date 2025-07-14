import cv2
import numpy as np
import math

# ✅ Function to calculate average brightness of the frame
def get_brightness(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = int(np.mean(gray))
    get_brightness.last_brightness = brightness
    return brightness

# Initialize last brightness value
get_brightness.last_brightness = 0

# ✅ Function to calculate Euclidean distance between two points
def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
