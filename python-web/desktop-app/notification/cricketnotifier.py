import datetime
import time
import requests
from plyer import notification

# Define the API URL and API Key as constants
API_URL = "https://api.cricapi.com/v1/currentMatches"
API_KEY = "f139597f-0a29-401a-926c-402a5d965851"  # Replace with your actual API key


def fetch_covid_stats():
    try:
        params = {
            "apikey": API_KEY,
            "offset": 0
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return []


def send_notification(match):
    innings = ''
    for score in match["score"]:
        innings += f"{score['inning']}:\n{score['r']}/{score['w']}  ({score['o']} overs)\n"

    if innings:
        notification_title = match['name']
        notification_message = f"Score:\n{innings}"

        notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon="icon.ico",
            app_name="Live Score, Worldcup 2023",
            timeout=600
        )


def main():
    matches = fetch_covid_stats()

    while True:
        current_date = datetime.date.today()
        for match in matches:
            match_date = datetime.datetime.strptime(match['date'], '%Y-%m-%d').date()

            if match_date == current_date and match['series_id'] == 'bd830e89-3420-4df5-854d-82cfab3e1e04' and not \
            match['matchEnded']:
                send_notification(match)
                time.sleep(600)  # Sleep for 10 minutes before checking the next match

        # Sleep for 12 hours before checking matches again
        time.sleep(60 * 60 * 12)


if __name__ == "__main__":
    main()
