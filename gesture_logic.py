import cv2
import mediapipe as mp
import time
from automation.copy_paste import perform_action

DEBUG = True

# Gesture thresholds
PINCH_THRESHOLD = 45
SPREAD_THRESHOLD = 160
DELTA_MIN = 10.0

# Activation rules
ROI_HOLD_REQUIRED = 0.30  # time (s) inside ROI to activate
COOLDOWN_SECONDS = 1.2    # between gestures
MAX_DURATION = 15         # auto-stop

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def compute_distance_and_points(hand_landmarks, frame_shape):
    h, w, _ = frame_shape

    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]

    x4, y4 = int(thumb_tip.x * w), int(thumb_tip.y * h)
    x8, y8 = int(index_tip.x * w), int(index_tip.y * h)

    distance = ((x8 - x4)**2 + (y8 - y4)**2)**0.5
    mid_x, mid_y = (x4 + x8) // 2, (y4 + y8) // 2

    return distance, (x4, y4), (x8, y8), (mid_x, mid_y)


def is_in_roi(mid_point, frame_shape):
    h, w, _ = frame_shape
    mid_x, mid_y = mid_point

    left = int(w * 0.35)
    right = int(w * 0.65)
    top = int(h * 0.35)
    bottom = int(h * 0.75)

    inside = left <= mid_x <= right and top <= mid_y <= bottom
    return inside, (left, top, right, bottom)


def main():
    cap = cv2.VideoCapture(0)

    start = time.time()
    last_event_time = 0

    state = "rest"          # rest / active
    prev_distance = None
    roi_entry_time = None   # used to activate inside ROI

    with mp_hands.Hands(max_num_hands=1) as hands:
        while True:

            # auto-stop
            if time.time() - start > MAX_DURATION:
                print("Session timeout reached, exiting.")
                break

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            event = None
            roi_box = None

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]

                distance, thumb_px, index_px, mid_px = compute_distance_and_points(
                    hand_landmarks, frame.shape
                )

                in_roi, roi_box = is_in_roi(mid_px, frame.shape)

                if DEBUG:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    cv2.circle(frame, thumb_px, 8, (255, 0, 0), -1)
                    cv2.circle(frame, index_px, 8, (0, 255, 0), -1)
                    cv2.circle(frame, mid_px, 6, (0, 255, 255), -1)

                # -----------------------------------------
                # ACTIVATION LOGIC (enter ROI → activate)
                # -----------------------------------------
                now = time.time()

                if in_roi:
                    if roi_entry_time is None:
                        roi_entry_time = now

                    if state == "rest" and now - roi_entry_time >= ROI_HOLD_REQUIRED:
                        state = "active"
                        print("Activation zone entered. Gesture mode ON.")

                else:
                    # leaving ROI instantly disables gestures
                    roi_entry_time = None
                    if state == "active":
                        print("Left activation zone. Gesture mode OFF.")
                    state = "rest"
                    prev_distance = None
                    continue

                # -----------------------------------------
                # GESTURE DETECTION ONLY IF ACTIVE
                # -----------------------------------------
                if state == "active":

                    if prev_distance is not None:
                        delta = abs(distance - prev_distance)
                    else:
                        delta = 0

                    # pinch → copy
                    if distance < PINCH_THRESHOLD and delta > DELTA_MIN:
                        if now - last_event_time > COOLDOWN_SECONDS:
                            event = "copy"
                            last_event_time = now

                    # spread → paste
                    elif distance > SPREAD_THRESHOLD and delta > DELTA_MIN:
                        if now - last_event_time > COOLDOWN_SECONDS:
                            event = "paste"
                            last_event_time = now

                    prev_distance = distance

                    if event:
                        print(f"Gesture event: {event} "
                              f"(distance={distance:.2f}, delta={delta:.2f})")

            # DEBUG drawing
            if DEBUG:
                if roi_box:
                    l, t, r, b = roi_box
                    cv2.rectangle(frame, (l, t), (r, b), (255, 255, 0), 2)

                cv2.putText(frame, f"Mode: {state}", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                cv2.imshow("Gesture Mode", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
