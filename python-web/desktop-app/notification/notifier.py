# importing required modules and libraries
import datetime  # to read present date
import time  # to suspend the execution for a specific time

import requests  # to retrieve COVID stats from web
from plyer import notification  # to get notification on the computer

# initializing a variable with None (temporary)
# indicating that there is no data available currently
covidStats = None
try:
    covidStats = requests.get("https://api.rootnet.in/covid19-in/stats/latest")
except:
    # in case the data is not fetched due to lack of internet
    print("Consider Checking the internet connection")

# in case we fetched data
if (covidStats != None):
    # converting data into JSON format
    jsonData = covidStats.json()['data']

    # repeating the loop for multiple times
    while (True):
        notification.notify(
            # defining the title of the notification,
            title="COVID19 Stats on {}".format(datetime.date.today()),
            # defining the message of the notification
            message="Total cases : {totalcases}\nToday cases : {todaycases}\nToday deaths : {todaydeaths}\nTotal active : {active}".format(
                totalcases=jsonData['summary']['total'],
                todaycases=jsonData['summary']['confirmedCasesIndian'],
                todaydeaths=jsonData['summary']['deaths'],
                active=jsonData['summary']["discharged"]),
            # creating icon for the notification
            # we have to download a icon of ico file format
            app_icon="icon.ico",
            # the notification stays for 30 seconds
            timeout=60
        )
        # sleep for 12 hrs => 60 * 60 * 12 seconds
        # notification repeats after every 12 hours
        time.sleep(60)
