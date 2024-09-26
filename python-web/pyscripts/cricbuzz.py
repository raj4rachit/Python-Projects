import json
import time
import urllib.request
from urllib.request import urlopen

import pyrebase
import schedule
import xmltodict

config = {
    "apiKey": "****",
    "authDomain": "****.firebaseapp.com",
    "databaseURL": "https://****.firebaseio.com",
    "storageBucket": "****.appspot.com"
}


def loadRSS():
    url = 'http://static.cricinfo.com/rss/livescores.xml'
    request_headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "http://thewebsite.com",
        "Connection": "keep-alive"
    }

    resp = urllib.request.Request(url, headers=request_headers)
    resp = urlopen(resp).read()
    return resp


def writeToFirebase(newsInJSON):
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child("News").child("CricketNews").set(newsInJSON)


def main():
    xmlContent = loadRSS()
    data = xmltodict.parse(xmlContent, xml_attribs=True)
    newsInJSON = json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))
    print(newsInJSON)
    # writeToFirebase(json.dumps(newsInJSON))


# main()
schedule.every(1).minutes.do(main)
"""schedule.every(1).minutes.do(main)
schedule.every().hour.do(main)
schedule.every().day.at("10:30").do(main)
schedule.every().monday.do(main)
schedule.every().wednesday.at("13:15").do(main)"""

while True:
    schedule.run_pending()
    time.sleep(1)
