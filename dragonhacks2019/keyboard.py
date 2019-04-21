from pynput.keyboard import Key,  Controller


import time

keyboard = Controller()


def action(command):



def forward():
    keyboard.press(Key.right)
    keyboard.release(getattr(Key, 'right'))

def backward():
    keyboard.press(Key.left)
    keyboard.release(Key.left)



def main():
    time.sleep(10)
    forward()
    time.sleep(5)
    backward()
main()
