from tkinter import messagebox

import requests
from new_app import common_function


class User:
    def __init__(self):
        self.base_url = "https://hrms-react.schedulesoftware.net/api"  # Replace with your server's URL

    def login(self, username, password):
        # Make a request to the server for user authentication
        response = requests.post(f"{self.base_url}/login", json={"email": username, "password": password})
        return response.json()

    def get_profile(self, token):
        if common_function.checkToken(token):
            # Get user profile from the server
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{self.base_url}/common-settings/refresh-token", headers=headers)
            response_data=response.json()
            profileData = None
            if response_data.get("status"):
                profileData = response_data.get("data")['user']
            else:
                messagebox.showerror("Error", response_data.get("error"))
            return profileData

class AuthenticationError(Exception):
    pass
