print("************************************************************************")
print("**********Property of Electronics For You Magazine and Associates*******")
print("*************************www.electronicsforu.com************************")
print("******************---------------------------------------***************")
print("*****************| Python Script for HotKey Emulation    |**************")
print("******************---------------------------------------***************")
print("****Code by Vijaykumar Sajjanar,hi.vjkr@gmail.com, +91-9980677175*******")
print("************************************************************************")
print("------------------------------------------------------------------------")
print("---Press Left Control Key to emulate Copy&Paste functions alternately--")
print("--------------------Close this window to stop Simulation----------------")
print("------------------------------------------------------------------------")
# Define the correct PINs
correct_pins = ['0000', '1111', '1234', '2024', '2025']


# Function to prompt for the PIN
def get_pin():
    pin = input("Enter a 4-digit PIN: ")
    return pin


# Ask for the PIN
while True:
    entered_pin = get_pin()
    if entered_pin in correct_pins:
        print("PIN accepted. Starting hotkey emulation.")
        break
    else:
        print("Incorrect PIN. Try again.")

from pynput import keyboard
from pynput.keyboard import Key, Controller

keyboard_ctrl = Controller()


def emulate_copy_paste(copy_mode):
    if copy_mode:
        # emulate Ctrl+C
        print("emulating Ctrl+C.")
        keyboard_ctrl.press(Key.ctrl)
        keyboard_ctrl.press('c')
        keyboard_ctrl.release('c')
        keyboard_ctrl.release(Key.ctrl)
    else:
        # emulate Ctrl+V
        print("emulating Ctrl+V.")
        keyboard_ctrl.press(Key.ctrl)
        keyboard_ctrl.press('v')
        keyboard_ctrl.release('v')
        keyboard_ctrl.release(Key.ctrl)


# Global variables
copy_mode = True
waiting_for_ctrl = False


def on_press(key):
    global copy_mode, waiting_for_ctrl

    try:
        if key == Key.ctrl_l and not waiting_for_ctrl:
            # If left control key is pressed and not waiting_for_ctrl, emulate copy
            emulate_copy_paste(copy_mode)
            # Toggle the mode
            copy_mode = not copy_mode
            # Set waiting_for_ctrl to True to wait for the next left control key press
            waiting_for_ctrl = True
    except AttributeError:
        pass


def on_release(key):
    global waiting_for_ctrl

    try:
        if key == Key.ctrl_l:
            # If left control key is released, set waiting_for_ctrl to False
            waiting_for_ctrl = False
    except AttributeError:
        pass


# Set up listeners
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()