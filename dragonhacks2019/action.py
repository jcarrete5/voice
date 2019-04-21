import time
from pynput.keyboard import Key, KeyCode, Controller
from config import Config

controller = Controller()


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


if __name__ == '__main__':
    a = 'shift+a'
    time.sleep(5)
    do_action(a)
