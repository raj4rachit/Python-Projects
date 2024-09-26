import datetime
import os
import threading
import time
import tkinter as tk
from functools import partial
from PIL import Image, ImageTk, ImageGrab

import pyautogui
import requests

# Global variables
logged_in = False
stop_thread = False
api_host = "https://hrms-react.schedulesoftware.net/api"

# Global variables for entry fields
username_entry = None
password_entry = None
activity_data = []



def create_login_window(parent):
    global login_message_var, username_entry, password_entry
    try:
        login_window = tk.Toplevel(parent)
        login_window.geometry("800x600")
        login_window.title("Login")

        # Open and convert the image to PhotoImage using PIL
        background_image_pil = Image.open("default_background.jpg")
        background_image = ImageTk.PhotoImage(background_image_pil)

        # Create a label to display the background image
        background_label = tk.Label(login_window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame for login elements
        login_frame = tk.Frame(login_window)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Display login page message
        login_message_var = tk.StringVar()  # StringVar to manage dynamic text
        login_message = tk.Label(login_frame, textvariable=login_message_var, fg="red")
        login_message.pack()

        # Username field
        username_label = tk.Label(login_frame, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(login_frame)
        username_entry.pack()

        # Password field
        password_label = tk.Label(login_frame, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(login_frame, show="*")
        password_entry.pack()

        # Login button
        login_button = tk.Button(login_frame, text="Login", command=login)
        login_button.pack()
    except Exception as e:
        print("Error loading image:", e)

def start_monitoring_window(parent):
    global monitoring_window, user_data

    monitoring_window = tk.Toplevel(parent)
    monitoring_window.geometry("800x600")
    monitoring_window.title("User Activity Monitoring")

    # Open and convert the image to PhotoImage using PIL
    background_image_pil = Image.open("default_background.jpg")
    background_image = ImageTk.PhotoImage(background_image_pil)

    # Create a label to display the background image
    background_label = tk.Label(monitoring_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Display user data
    user_data_label = tk.Label(monitoring_window, text=f"User Data: {user_data}")
    user_data_label.pack()

    for key, value in user_data['user'].items():
        user_data_entry = tk.Label(monitoring_window, text=f"{key}: {value}")
        user_data_entry.pack()

    # Display monitoring message
    monitor_message = tk.Label(monitoring_window, text="Monitoring user activity...")
    monitor_message.pack()

    # Store the label in a global variable for later updates
    global monitor_label
    monitor_label = monitor_message

    # Add a logout button
    logout_button = tk.Button(monitoring_window, text="Logout", command=logout)
    logout_button.pack()

    # Start monitoring thread
    start_monitoring_thread()

def logout():
    global logged_in
    logged_in = False
    monitoring_window.destroy()  # Close the monitoring window
    login_window.deiconify()  # Show the login window
    login_message_var.set("")


def login():
    global logged_in, login_message_var, user_data, username_entry, password_entry, login_window
    username = username_entry.get()
    password = password_entry.get()

    # Display login message
    login_message_var.set("Logging in... Please wait.")  # Update the text dynamically

    # Authenticate the user using the API
    if username == '' or password == '':
        login_message_var.set("Please enter email address or password.")
    else:
        success, data = authenticate_user(username, password)
        if success:
            logged_in = True
            user_data = data  # Store user data for later use
            start_monitoring_window(login_window)

def authenticate_user(username, password):
    api_url = f"{api_host}/login"
    data = {"email": username, "password": password}

    response = requests.post(api_url, data=data)

    # Write API response into a log file
    log_api_response(response)

    if response.status_code == 200:
        response_data = response.json()  # Retrieve the JSON data from the response
        if response_data.get("status"):
            return True, response_data.get("data")  # Authentication successful
        else:
            if response_data.get("data"):
                login_message_var.set(response_data.get("data")['email'])
            else:
                login_message_var.set(response_data.get("error"))
            return False, None  # Authentication failed
    else:
        return False, None  # Authentication failed

def start_monitoring_thread():
    global stop_thread
    stop_thread = False
    monitoring_thread = threading.Thread(target=monitor_activity)
    monitoring_thread.start()

    # Start the timer to send data to the server
    start_data_send_timer()

    # Display monitoring message
    monitor_label.config(text="Monitoring user activity...")


def start_data_send_timer():
    data_send_timer = threading.Timer(60, send_activity_data)  # Send data every 1 minute
    data_send_timer.start()

def send_activity_data():
    global activity_data
    if activity_data:
        # Send activity_data to the server (you need to implement this part)
        send_activity_data(activity_data)
        activity_data = []  # Clear the collected data

    # Start the timer again for the next data sending interval
    start_data_send_timer()

def monitor_activity():
    while not stop_thread:
        if logged_in:
            # Capture the screen
            current_time = datetime.datetime.now()
            ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
            # screenshot = ImageGrab.grab()
            screenshot = pyautogui.screenshot()

            filename = f"screenshots/my_screenshot_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.png"

            # Create the "screenshots" folder if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)

            screenshot.save(filename)
            # Save or process the screenshot as needed
            activity_data.append({
                'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'screenshot_filename': filename
            })

            # Log user activity (you need to implement this part)
            log_activity("User performed an action")

        # Adjust the time interval as needed
        time.sleep(60)  # Capture screen every 5 seconds


def log_api_response(response):
    with open("activity_log.txt", "a") as log_file:
        log_file.write("Response Status Code: {}\n".format(response.status_code))
        log_file.write("Response Content: {}\n".format(response.content))
        log_file.write("\n")


def log_activity(activity):
    timestamp = datetime.datetime.now()
    # Implement activity logging (e.g., writing to a log file or database)
    # You can include the timestamp along with the activity description
    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{formatted_timestamp}: {activity}"

    with open("activity_log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")

def main():
    global login_window

    login_window = tk.Tk()  # Create the main login window
    login_window.geometry("800x600")
    login_window.title("Main Window")

    # Load the favicon ICO image
    favicon_image = Image.open("icon.ico")
    favicon = ImageTk.PhotoImage(favicon_image)

    # Call the Tcl/Tk command to set the icon using the PhotoImage
    login_window.call('wm', 'iconphoto', login_window._w, favicon)

    # Create a frame for main window elements
    main_frame = tk.Frame(login_window)
    main_frame.pack(expand=True)

    # Add buttons to open login and monitoring windows
    login_button = tk.Button(main_frame, text="Login", command=lambda: create_login_window(login_window))
    login_button.pack()

    monitoring_button = tk.Button(main_frame, text="Start Monitoring", command=lambda: start_monitoring_window(login_window))
    monitoring_button.pack()

if __name__ == "__main__":
    main()
    login_window.mainloop()