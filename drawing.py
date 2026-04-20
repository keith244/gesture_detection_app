import cv2
import mediapipe as mp
import pyautogui
import time

# ── MediaPipe setup ────────────────────────────────────────────────
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# ── Tuning knobs ───────────────────────────────────────────────────
VELOCITY_THRESHOLD  = 0.004   # minimum speed per frame to count as a spike
REVERSAL_THRESHOLD  = 0.02    # minimum speed for a reversal to count (filters noise)
CONSECUTIVE_FRAMES  = 1       # how many fast frames in a row to confirm swipe
DIRECTION_TOLERANCE = 3       # frames allowed to change direction mid-swipe before cancelling
COOLDOWN            = 1.0     # seconds to ignore input after swipe fires

# ── State machine ──────────────────────────────────────────────────
WAITING    = "waiting"
MEASURING  = "measuring"

state              = WAITING
prev_y             = None
prev_velocity      = None
turning_point_y    = None
consecutive_count  = 0
spike_direction    = None
last_swipe_time    = 0
direction_breaks   = 0

# ── Camera ─────────────────────────────────────────────────────────
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

            finger_y = hand_landmarks.landmark[8].y

            if prev_y is not None:
                velocity = finger_y - prev_y

                now = time.time()

                # ── WAITING: looking for a real direction reversal ─────
                if state == WAITING:
                    if prev_velocity is not None:
                        real_reversal = (
                            (prev_velocity > REVERSAL_THRESHOLD and velocity < -REVERSAL_THRESHOLD) or
                            (prev_velocity < -REVERSAL_THRESHOLD and velocity > REVERSAL_THRESHOLD)
                        )
                        if real_reversal:
                            print(f"REVERSAL DETECTED | velocity: {velocity:.4f}")
                            turning_point_y   = finger_y
                            spike_direction   = "down" if velocity > 0 else "up"
                            consecutive_count = 1       # seed with this strong frame
                            state             = MEASURING

                # ── MEASURING: looking for fast consistent spike ───────
                elif state == MEASURING:
                    print(f"MEASURING | velocity: {velocity:.4f} | consec: {consecutive_count} | direction: {spike_direction}")

                    if abs(velocity) >= VELOCITY_THRESHOLD:
                        direction = "down" if velocity > 0 else "up"

                        if direction == spike_direction:
                            consecutive_count += 1
                            direction_breaks = 0  # reset if back on track
                        else:
                            # direction changed — allow some tolerance
                            direction_breaks += 1
                            if direction_breaks > DIRECTION_TOLERANCE:
                                print("CANCELLED | direction changed mid-swipe")
                                state             = WAITING
                                consecutive_count = 0
                                spike_direction   = None
                                direction_breaks  = 0

                        if consecutive_count >= CONSECUTIVE_FRAMES:
                            if now - last_swipe_time > COOLDOWN:
                                if spike_direction == "down":
                                    print("SWIPE DOWN → Next video")
                                    pyautogui.press('down')
                                else:
                                    print("SWIPE UP → Previous video")
                                    pyautogui.press('up')
                                last_swipe_time = now

                            # reset regardless
                            state             = WAITING
                            consecutive_count = 0
                            spike_direction   = None
                            direction_breaks  = 0

                    else:
                        # finger slowed down before confirming — cancel
                        print(f"CANCELLED | velocity too slow: {velocity:.4f}")
                        state             = WAITING
                        consecutive_count = 0
                        spike_direction   = None
                        direction_breaks  = 0

                prev_velocity = velocity

            prev_y = finger_y

            # ── HUD ───────────────────────────────────────────────────
            cv2.putText(frame, f"State: {state}",              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Finger Y: {finger_y:.3f}",    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Consec: {consecutive_count}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()