import cv2
import mediapipe as mp
import time

DEBUG = False  # change to False when you don't want to see the camera window

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)  # 0 = default webcam


start_time = time.time()
MAX_DURATION = 30 

with mp_hands.Hands(max_num_hands=1) as hands:
    while True:

         # --- auto stop after MAX_DURATION seconds ---
        if time.time() - start_time > MAX_DURATION:
            print("Time limit reached, exiting...")
            break
        # -------------------------------------------- 



        ret, frame = cap.read()
        if not ret:
            break

        # Flip so it feels like a mirror
        frame = cv2.flip(frame, 1)

        # Convert to RGB for MediaPipe
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # Draw landmarks if any hand found
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        if DEBUG:
            cv2.imshow("Hand Tracking", frame)

        # ESC to quit
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
