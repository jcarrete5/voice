import time
from pynput.keyboard import Key, KeyCode, Controller
import pynput.mouse as ms
from config import Config
import tkinter as tk

controller = Controller()
mouse = ms.Controller()

def do_actions(*actions: list, cfg: Config = None):
    """
    Perform actions from actions list in sequence
    """
    is_meta = False
    for action in actions:
        is_meta = any((do_action(action, cfg), is_meta))
    return is_meta


def do_action(action: str, cfg: Config = None) -> bool:
    if action.startswith('##'):
        do_meta_action(action, cfg)
        return True
    else:
        tokens = action.split('+')
        for token in tokens:
            if (token.startswith("mouse")):
                mouse_cmd: str = token.split('.')[1]
                tokens.remove(token)

                if mouse_cmd.startswith("move"):
                    coords = mouse_cmd.replace("move(", "").replace(")", "").split(',')

                    m_pos = mouse.position
                    coords = get_coords(int(coords[0]), int(coords[1]))

                    mouse.move(coords[0] - m_pos[0], coords[1] - m_pos[1])
                elif mouse_cmd == "rclick":
                    mouse.click(ms.Button.right, 1)
                elif mouse_cmd == "lclick":
                    mouse.click(ms.Button.left, 1)
            else:
                controller.press(getattr(Key, token, KeyCode.from_char(token)))
        for token in reversed(tokens):
            controller.release(getattr(Key, token, KeyCode.from_char(token)))
    return False


def do_meta_action(meta_action: str, cfg: Config):
    if meta_action == '##next_scope':
        return cfg.next_scope()
    elif meta_action == '##prev_scope':
        return cfg.prev_scope()
    elif meta_action.startswith('##delay'):
        ms = int(meta_action.split(',')[1])
        time.sleep(ms / 1000)
    elif meta_action.startswith('##print'):
        s = meta_action.split(',')[1]
        print(s)
    else:
        raise RuntimeError(f'Invalid meta action: {meta_action}')


root=tk.Tk()
def get_coords(x, y):
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    x = x/1920 * screen_w
    y = y/1080 * screen_h
    return (x, y)

if __name__ == '__main__':
    a = 'shift+a'
    time.sleep(5)
    do_action(a)
