import cv2
import mediapipe as mp
import pyautogui
import time
import platform

# Optional: brightness control for Windows
if platform.system() == 'Windows':
    import screen_brightness_control as sbc

from gesture_utils import get_brightness, calculate_distance

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

prev_gesture = None
gesture_cooldown = 1  # seconds
last_action_time = 0

def detect_gestures(img):
    global prev_gesture, last_action_time

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    h, w, _ = img.shape

    gesture = "None"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            lm_pos = [(int(lm[i].x * w), int(lm[i].y * h)) for i in range(21)]

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers = []
            fingers.append(1 if lm[4].x < lm[3].x else 0)  # Thumb
            fingers.append(1 if lm[8].y < lm[6].y else 0)  # Index
            fingers.append(1 if lm[12].y < lm[10].y else 0)  # Middle
            fingers.append(1 if lm[16].y < lm[14].y else 0)  # Ring
            fingers.append(1 if lm[20].y < lm[18].y else 0)  # Pinky

            total_fingers = sum(fingers)

            brightness = get_brightness(img)

            # === GESTURE DETECTION ===
            if fingers == [1, 1, 1, 1, 1]:
                gesture = "Open Palm"
            elif fingers == [0, 0, 0, 0, 0]:
                gesture = "Fist"
            elif fingers == [1, 0, 0, 0, 0]:
                gesture = "Volume Up"
            elif fingers == [0, 0, 0, 0, 1]:
                gesture = "Volume Down"
            elif fingers == [0, 1, 0, 0, 0]:
                gesture = "Left Click"
            elif fingers == [0, 1, 1, 0, 0]:
                gesture = "Double Click"
            elif calculate_distance(lm_pos[4], lm_pos[8]) < 30:
                gesture = "Copy"
            elif fingers == [1, 0, 0, 0, 1]:
                gesture = "Paste"
            elif fingers == [0, 1, 1, 1, 1]:
                gesture = "Brightness Up"
            elif fingers == [0, 0, 1, 0, 0]:
                gesture = "Middle Finger"
            else:
                gesture = "Unknown"

            # === ACTIONS ===
            current_time = time.time()
            if gesture != prev_gesture or (current_time - last_action_time > gesture_cooldown):
                execute_gesture_action(gesture)
                prev_gesture = gesture
                last_action_time = current_time

            detect_gestures.last_gesture = gesture
            cv2.putText(img, f"Gesture: {gesture}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        detect_gestures.last_gesture = "No Hand"

    return img

# System control based on gesture
def execute_gesture_action(gesture):
    print(f"[ACTION] {gesture}")
    try:
        if gesture == "Volume Up":
            pyautogui.press("volumeup")
        elif gesture == "Volume Down":
            pyautogui.press("volumedown")
        elif gesture == "Left Click":
            pyautogui.click()
        elif gesture == "Double Click":
            pyautogui.doubleClick()
        elif gesture == "Copy":
            pyautogui.hotkey("ctrl", "c")
        elif gesture == "Paste":
            pyautogui.hotkey("ctrl", "v")
        elif gesture == "Brightness Up":
            if platform.system() == "Windows":
                current = sbc.get_brightness()[0]
                sbc.set_brightness(min(100, current + 10))
        elif gesture == "Fist":
            pass  # placeholder, could use for locking, pause, etc.
    except Exception as e:
        print(f"⚠️ Failed to execute action: {e}")

detect_gestures.last_gesture = "None"
