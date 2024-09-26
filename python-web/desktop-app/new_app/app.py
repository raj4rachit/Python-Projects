import requests
from new_app import common_function

class App:
    def __init__(self):
        self.base_url = "https://hrms-react.schedulesoftware.net/api"  # Replace with your server's URL

    def refersh_data(self, token):
        if common_function.checkToken(token):
            # Get application refersh data from the server
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{self.base_url}/common-settings/refresh-token", headers=headers)
            return response.json()
