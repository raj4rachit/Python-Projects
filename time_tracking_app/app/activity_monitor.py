import time
import os
from datetime import datetime
from app import db
from app.models import Activity, User


def capture_screenshot():
    # Implement screenshot capture logic
    screenshot_path = f'screenshots/{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.png'
    # Save the screenshot to the path
    return screenshot_path


def capture_active_window():
    # Implement logic to capture the active window title
    active_window = "Dummy Active Window"  # Replace with actual active window title
    return active_window


def track_activity(user_id):
    screenshot_path = capture_screenshot()
    active_window = capture_active_window()
    keyboard_events = 0  # Replace with actual keyboard event count
    mouse_events = 0  # Replace with actual mouse event count

    activity = Activity(
        user_id=user_id,
        screenshot=screenshot_path,
        active_window=active_window,
        keyboard_events=keyboard_events,
        mouse_events=mouse_events
    )
    db.session.add(activity)
    db.session.commit()


def monitor_user_activity():
    users = User.query.all()
    for user in users:
        track_activity(user.id)
    time.sleep(300)  # Sleep for 5 minutes
