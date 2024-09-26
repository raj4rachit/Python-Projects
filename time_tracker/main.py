import tkinter as tk
import requests


class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")

        self.login_frame = tk.Frame(self.master)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()

        self.login_frame.pack()

        self.user_frame = tk.Frame(self.master)
        self.user_data_label = tk.Label(self.user_frame, text="User Data:")
        self.user_data_label.pack()
        self.user_data_text = tk.Text(self.user_frame, height=30, width=80)
        self.user_data_text.pack()
        self.user_frame.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Make a request to your API for user authentication
        response = requests.post("https://hrms.schedulesoftware.net/api/login",json={"email": username, "password": password})

        if response.status_code == 200:
            try:
                # Try to get response data
                data = response.json()
                if data["status"]:
                    print("Login successful")
                    # Hide login frame
                    self.login_frame.pack_forget()
                    # Display user data with proper formatting
                    formatted_data = ""
                    for key, value in data.items():
                        formatted_data += f"{key}: {value}\n"
                    self.user_data_text.insert(tk.END, formatted_data)
                else:
                    print("Login failed")
                # Here you can open another window or perform any other action
            except ValueError:
                # Response data is not in JSON format
                print("Response data is not in JSON format")
        else:
            # Login failed
            print("Login failed")


def main():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
