# Import the relevant modules
from functools import partial

import pyautogui
from PIL import ImageGrab

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
#
# # Spiral drawing using pyautogui
# time.sleep(3)
# distance = 300
#
# while distance > 0:
#     pyautogui.dragRel(distance, 0, button="left")
#     distance = distance - 20
#     pyautogui.dragRel(0, distance, button="left")
#     pyautogui.dragRel(-distance, 0, button="left")
#     distance = distance - 20
#     pyautogui.dragRel(0, -distance, button="left")
#     # time.sleep(2)

im1 = pyautogui.screenshot()
im1.save('my_screenshot.png')
