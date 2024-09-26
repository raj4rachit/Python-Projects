import json
import time
import threading
from functools import partial

import pyautogui
from win32gui import GetForegroundWindow, GetWindowText
import psutil
import win32process
import pygetwindow as gw
import requests
from PIL import ImageGrab
import os
import re

process_time = {}
timestamp = {}
data_dict = {}

def get_active_window_title():
    hwnd = GetForegroundWindow()
    return GetWindowText(hwnd)

def get_chrome_url():
    windows = gw.getWindowsWithTitle(" - Google Chrome")
    if windows:
        return windows[0].title.replace(" - Google Chrome", "")
    return "N/A"

def get_firefox_url():
    windows = gw.getWindowsWithTitle(" - Mozilla Firefox")
    if windows:
        return windows[0].title.replace(" - Mozilla Firefox", "")
    return "N/A"

def save_data_to_json(data):
    with open('app_usage_data.json', 'w') as json_file:
        json.dump(list(data.values()), json_file, indent=4)

def send_data_to_api(data):
    api_url = "http://your_api_endpoint"  # Replace with your actual API endpoint
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json=list(data.values()), headers=headers)
    return response.status_code, response.text

def sanitize_filename(title):
    # Replace invalid characters with an underscore
    return re.sub(r'[<>:"/\\|?*]', '_', title)

def capture_screenshots():
    screenshot_dir = 'screenshots'
    os.makedirs(screenshot_dir, exist_ok=True)
    ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
    screenshot = pyautogui.screenshot()
    timestamp = int(time.time())
    screenshot_path = os.path.join(screenshot_dir, f"{timestamp}.png")
    screenshot.save(screenshot_path, format="PNG")

    # windows = gw.getAllWindows()
    # for window in windows:
    #     if window.visible:
    #         bbox = window.box
    #         # Calculate right and bottom coordinates
    #         right = bbox[0] + bbox[2]
    #         bottom = bbox[1] + bbox[3]
    #         # Validate the bounding box
    #         if right > bbox[0] and bottom > bbox[1]:
    #             screenshot = ImageGrab.grab(bbox=(bbox[0], bbox[1], right, bottom),all_screens=True)
    #             sanitized_title = sanitize_filename(window.title)
    #             screenshot_path = os.path.join(screenshot_dir, f"{sanitized_title}.png")
    #             screenshot.save(screenshot_path, format="PNG")
    #             print(f"Captured screenshot of window: {window.title}")
    #             # Add screenshot path to data_dict
    #             key = (window.title, window.title)  # Using window title as both app_name and active_window_title for simplicity
    #             if key in data_dict:
    #                 data_dict[key]['screenshot_path'] = screenshot_path
    #             else:
    #                 data_dict[key] = {
    #                     "app_name": window.title,
    #                     "usage_time": 0,  # Initialize with 0 for simplicity
    #                     "active_window_title": window.title,
    #                     "url": "N/A",  # Default to N/A for simplicity
    #                     "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
    #                     "screenshot_path": screenshot_path
    #                 }
    #         else:
    #             print(f"Invalid bounding box for window: {window.title}, bbox: {bbox}")

def periodic_task():
    global data_dict
    save_data_to_json(data_dict)
    # status_code, response_text = send_data_to_api(data_dict)
    # print(f"Data sent to API. Status code: {status_code}, Response: {response_text}")
    capture_screenshots()  # Capture screenshots of all windows every 3 minutes
    threading.Timer(10, periodic_task).start()  # Schedule the task to run every 3 minutes

# Start the periodic task
periodic_task()

try:
    while True:
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
        timestamp[current_app] = int(time.time())
        time.sleep(1)

        if current_app not in process_time.keys():
            process_time[current_app] = 0
        process_time[current_app] = process_time[current_app] + int(time.time()) - timestamp[current_app]

        active_window_title = get_active_window_title()
        if "chrome" in current_app.lower():
            current_url = get_chrome_url()
        elif "firefox" in current_app.lower():
            current_url = get_firefox_url()
        else:
            current_url = "N/A"

        print(f"App: {current_app}, Time: {process_time[current_app]}, Title: {active_window_title}, URL: {current_url}")

        #capture_screenshots()
        # Update or add data for periodic JSON and API send
        key = (current_app, active_window_title)
        if key in data_dict:
            data_dict[key]['usage_time'] += int(time.time()) - timestamp[current_app]
            data_dict[key]['url'] = current_url
        else:
            data_dict[key] = {
                "app_name": current_app,
                "usage_time": process_time[current_app],
                "active_window_title": active_window_title,
                "url": current_url,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            }
        save_data_to_json(data_dict)
except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    print("Final process time data:", process_time)
