import time
from pynput.keyboard import Key, KeyCode, Controller
from config import Config

controller = Controller()


def do_actions(*actions: list, cfg: Config = None):
    """
    Perform actions from actions list in sequence
    """
    for action in actions:
        do_action(action, cfg)


def do_action(action: str, cfg: Config = None):
    if action.startswith('##'):
        do_meta_action(action, cfg)
    else:
        tokens = action.split('+')
        for token in tokens:
            controller.press(getattr(Key, action, KeyCode.from_char(token)))
        for token in tokens:
            controller.release(getattr(Key, action, KeyCode.from_char(token)))


def do_meta_action(meta_action: str, cfg: Config):
    if meta_action == '##next_scope':
        return cfg.next_scope()
    elif meta_action == '##prev_scope':
        return cfg.prev_scope()
    else:
        raise RuntimeError(f'Invalid meta action: {meta_action}')


if __name__ == '__main__':
    a = 'shift+a'
    time.sleep(5)
    do_action(a)
