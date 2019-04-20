from pynput.keyboard import Key, Controller

keyboard = Controller()

def forward():
    keyboard.press(Key.right)
    keyboard.release(Key.right)

def backward():
    keyboard.press(Key.left)
    keyboard.release(Key.left)

