from pynput import mouse

from pynput.keyboard import Controller

keyboard = Controller()


def on_move(x, y):
    print('Pointer moved to {0}'.format((x, y)))


def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        raise MyException(button)

    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False


def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))


# Collect events until released
class MyException(Exception):
    pass


with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    try:
        listener.join()
    except MyException as e:
        print('{0} was clicked'.format(e.args[0]))

# ...or, in a non-blocking fashion:
listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
listener.start()
