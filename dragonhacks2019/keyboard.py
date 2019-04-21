from pynput.keyboard import Key, KeyCode, Controller


import time

actionProcessor= Controller()

# input string and breaks up into array of strings to get keyboard action
def action(commandStrings):
    command=commandStrings.split('+')

    for instruction in command:
        actionProcessor.press(getattr(Key, instruction, KeyCode.from_char(instruction)))
    for instruction in command:
        actionProcessor.release(getattr(Key, instruction, KeyCode.from_char(instruction)))

next= 'right'
back= 'left'
a= 'shift+a'



if __name__ == '__main__':
    time.sleep(5)
    action(a)

