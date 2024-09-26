import tkinter as tk
from functools import partial
from tkinter import messagebox

import boto3
import botocore.exceptions

import pyautogui
from PIL import Image, ImageTk, ImageGrab  # Import PIL modules
from user import User, AuthenticationError
from app import App
from pynput import mouse, keyboard
import mss
import time
import os

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("HRMS Desktop App")

        # Load favicon image
        favicon = Image.open("images/favicon.ico")
        favicon = ImageTk.PhotoImage(favicon)
        self.root.iconphoto(False, favicon)  # Set the favicon

        self.user = User()
        self.app = App()

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.profile_data_var = tk.StringVar()
        self.token = None
        self.user_data = None

        self.app_data = None
        self.aws_settings = None
        self.tracker_settings = None
        self.timesheets = None
        self.tasks = None
        self.employee_data = None

        # Initialize monitor
        self.monitor = mss.mss()

        self.create_widgets()

        # Initialize mouse and keyboard listeners
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)

        # Initialize activity log file
        self.activity_log = open("monitor_log.txt", "a")  # Open in append mode

        # Start listeners (call these where appropriate)
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def create_widgets(self):
        # Login Screen
        self.login_frame = tk.Frame(self.root)
        self.login_frame.grid(padx=20, pady=20)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(self.login_frame, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, sticky="e", pady=10)
        self.password_entry = tk.Entry(self.login_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=10)

        # Profile Screen
        self.profile_frame = tk.Frame(self.root)
        self.profile_frame.grid(padx=20, pady=20)

        self.profile_label = tk.Label(self.profile_frame, text="Profile Data:")
        self.profile_label.grid(row=0, column=0)

        self.profile_text = tk.Text(self.profile_frame, height=10, width=40)
        self.profile_text.grid(row=1, column=0)

        self.logout_button = tk.Button(self.profile_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=2, column=0,padx=20)

        # Initially hide profile_frame
        self.profile_frame.grid_forget()

        # Start a timer to capture screenshots every 1 minute
        self.start_screenshot_timer()

    def login(self):
        try:
            if self.username_var.get() == '' or self.password_var.get() == '':
                messagebox.showerror("Error", "Please Enter Email Address or Password.")
            else:
                response_data = self.user.login(self.username_var.get(), self.password_var.get())
                if response_data.get("status"):
                    self.token = response_data.get("data")['token']
                    self.user_data = response_data.get("data")['user']
                    self.refresh_data()  # Call the refresh API
                    self.show_profile()
                    self.login_frame.grid_forget()  # Hide login_frame
                    self.save_screenshot()

                else:
                    if response_data.get("data"):
                        messagebox.showerror("Error", response_data.get("data")['email'])
                    else:
                        messagebox.showerror("Error", response_data.get("error"))
        except AuthenticationError:
            messagebox.showerror("Error", "Authentication failed.")

    def show_profile(self):
        profile_data = self.user.get_profile(self.token)
        self.profile_text.delete("1.0", tk.END)  # Clear previous data
        for key, value in profile_data.items():
            self.profile_text.insert(tk.END, f"{key}: {value}\n")

        self.profile_frame.grid(row=1, column=1,padx=20, pady=20)  # Show profile_frame

    def refresh_data(self):
        self.app_data = self.app.refersh_data(self.token)
        if self.app_data.get("status"):
            self.user_data = self.app_data.get("data")["user"]
            self.timesheets = self.app_data.get("data")["time_sheet"]
            self.tasks = self.app_data.get("data")["task"]
            self.aws_settings = self.app_data.get("data")["settings"]["screen_capture_configuration"]
            print(self.aws_settings['ss_access_key'])
        else:
            messagebox.showerror("Error", self.app_data.get("error"))

    def logout(self):
        self.save_screenshot()
        self.token = None
        self.user_data = None
        self.profile_text.delete("1.0", tk.END)
        self.username_var.set("")
        self.password_var.set("")
        self.profile_frame.grid_forget()
        self.login_frame.grid(row=1, column=1,padx=20, pady=20)

    def on_click(self, x, y, button, pressed):
        # Handle mouse click events
        action = f"Mouse Click: {'Pressed' if pressed else 'Released'} at ({x}, {y})\n"
        self.log_activity(action)

    def on_press(self, key):
        # Handle key press events
        try:
            action = f"Key Press: {key.char}\n"
        except AttributeError:
            action = f"Special Key Press: {key}\n"
        self.log_activity(action)

    def log_activity(self, action):
        # Write the action to the log file
        self.activity_log.write(action)

    def save_screenshot(self):
        # Generate a unique filename using a timestamp
        timestamp = int(time.time())

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
        screenshot = pyautogui.screenshot()
        filename = f"screenshots/my_screenshot_{timestamp}.png"

        # Create the "screenshots" folder if it doesn't exist
        os.makedirs("screenshots", exist_ok=True)
        screenshot.save(filename)

        # Upload the screenshot to S3
        #s3_filename = f"{self.aws_settings['ss_path']}/{self.aws_settings['ss_sub_path']}/{filename}"
        s3_filename = f"{self.aws_settings['ss_path']}/{filename}"
        s3_url = self.upload_to_s3(filename, s3_filename)
        if s3_url:
            print(f"Screenshot uploaded to: {s3_url}")

        self.screenshot_timer = time.time() + 60  # Schedule the next screenshot
        print(f"Screenshot captured and saved as {filename}")

    def start_screenshot_timer(self):
        # Schedule to capture a screenshot every 1 minute
        self.screenshot_timer = time.time() + 60  # 60 seconds = 1 minute
        self.refresh_timer = time.time()


    def upload_to_s3(self, local_filename, s3_filename):
        s3 = boto3.client(
            's3',
            aws_access_key_id=self.aws_settings['ss_access_key'],
            aws_secret_access_key=self.aws_settings['ss_secret_key'],
            region_name=self.aws_settings['ss_region']
        )

        try:
            s3.upload_file(local_filename, self.aws_settings['ss_bucket_name'], s3_filename, ExtraArgs={'ACL': self.aws_settings['ss_acl']})
            print(f"Uploaded {local_filename} to {s3_filename} on S3")
            s3_url = f"{self.aws_settings['ss_service_url']}/{self.aws_settings['ss_bucket_name']}/{s3_filename}"
            return s3_url
        except botocore.exceptions.NoCredentialsError:
            print("AWS credentials not available. Unable to upload to S3.")
            return None
        except Exception as e:
            print(f"An error occurred while uploading to S3: {e}")
            return None

    def run(self):
        def update():
            # Check if it's time to capture a screenshot
            if time.time() >= self.screenshot_timer and self.token:
                self.save_screenshot()
                self.screenshot_timer = time.time() + 60  # Schedule the next screenshot

            # Check if it's time to refresh data
            if time.time() >= self.refresh_timer and self.token:
                self.refresh_data()  # Call the refresh API
                self.refresh_timer = time.time() + 60  # Schedule the next refresh

            # Other application logic
            self.root.update_idletasks()
            self.root.update()
            time.sleep(1)  # Small delay to prevent high CPU usage

            # Schedule the next update after 1 second
            self.root.after(1000, update)  # 1000 ms = 1 second

        # Initialize refresh timer
        self.refresh_timer = time.time() + 60

        # Start the initial update
        update()

        # Start the tkinter main event loop
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
