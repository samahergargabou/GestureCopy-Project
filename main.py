from gesture_detection.gesture_logic import detect_gesture
from automation.copy_paste import perform_action

def main():
    while True:
        event = detect_gesture()
        if event:
            perform_action(event)

if __name__ == "__main__":
    main()
