from pynput import keyboard

# Initialize counters
key_press_count = 0
mouse_click_count = 0
last_key_press = ''


# The event listener will be running in this block
# with keyboard.Events() as events:
#     for event in events:
#         if event.key == keyboard.Key.esc:
#             break
#         else:
#             print('Received event {}'.format(event))
#             print(event.key)
#             print(event)
#

def on_press(key):
    global key_press_count, last_key_press
    try:
        if key.char != last_key_press:
            key_press_count += 1
        else:
            print('no key')
        last_key_press = key.char
        # print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        if key != last_key_press:
            key_press_count += 1
        # print('special key {0} pressed'.format(key))
        last_key_press = key


def on_release(key):
    global key_press_count
    # print('{0} released'.format(key))
    print('Key Press Count:', key_press_count)
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

# Print the counts
print('Key Press Count:', key_press_count)
print('Mouse Click Count:', mouse_click_count)
