import cv2
import mediapipe as mp
import pyautogui
from collections import deque
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

tip_history = deque(maxlen=20)
SWIPE_THRESHOLD = 0.15  # slightly lower since fingertips move more than wrist
last_swipe_time = 0
COOLDOWN = 1.0

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: could not open webcam")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_tip = hand_landmarks.landmark[8]
            tip_history.append(index_tip.y)

            if len(tip_history) >= 20:
                history_list = list(tip_history)

                # Split into first and second half
                first_half = history_list[:10]
                second_half = history_list[10:]

                avg_start = sum(first_half) / len(first_half)
                avg_end = sum(second_half) / len(second_half)

                # positive delta = moved down (Y increases downward)
                # negative delta = moved up
                delta = avg_end - avg_start
                now = time.time()

                if now - last_swipe_time > COOLDOWN:
                    if delta > SWIPE_THRESHOLD:
                        print("SWIPE DOWN -> Next video")
                        pyautogui.press('down')
                        tip_history.clear()
                        last_swipe_time = now
                    elif delta < -SWIPE_THRESHOLD:
                        print("SWIPE UP -> Previous video")
                        pyautogui.press('up')
                        tip_history.clear()
                        last_swipe_time = now

            cv2.putText(frame, f"Index tip Y: {index_tip.y:.3f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()