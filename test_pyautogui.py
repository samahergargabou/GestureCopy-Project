# automation/test_pyautogui.py

import time
import pyautogui

print("You have 5 seconds to focus a text field (e.g., Notepad) and leave the cursor there...")
time.sleep(10)

print("Typing...")
pyautogui.typewrite("Hello from pyautogui!", interval=0.05)

print("Done.")
