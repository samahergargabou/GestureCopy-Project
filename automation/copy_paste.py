import time
import pyautogui


def perform_action(event: str) -> None:
    """
    event: 'copy' or 'paste'
    """
    if event == "copy":
        pyautogui.hotkey("ctrl", "c")
    elif event == "paste":
        pyautogui.hotkey("ctrl", "v")
    else:
        return

    time.sleep(0.1)


if __name__ == "__main__":
    print("You have 7 seconds to select some text (in Notepad, browser, etc.)...")
    time.sleep(7)

    print("Sending COPY (Ctrl+C)...")
    perform_action("copy")

    print("Now click in an empty text field. You have 3 seconds...")
    time.sleep(3)

    print("Sending PASTE (Ctrl+V)...")
    perform_action("paste")

    print("Done.")

