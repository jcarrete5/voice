import sys
import pathlib
import os
import action
from argparse import ArgumentParser
from config import Config
from speech_to_text import SpeechToTextClient

parser = ArgumentParser()
parser.add_argument('-c', '--config', required=True)
args = parser.parse_args(sys.argv[1:])
cfg = Config(args.config)
seen_phrases = set()
secret_path = os.path.abspath('secret.json')
stt = SpeechToTextClient(secret_path, 'en-US', cfg.phrases())


def phrase_parser(phrase):
    phrase, is_final = phrase
    print(phrase)
    for known_phrase in cfg.phrases():
        if known_phrase not in seen_phrases and known_phrase in phrase:
            seen_phrases.add(known_phrase)
            executed_meta = action.do_actions(*cfg.actions(known_phrase), cfg=cfg)
            if executed_meta:
                stt.update_phrase_hints(cfg.phrases())
                seen_phrases.clear()
                stt.restart(phrase_parser)
    if is_final:
        seen_phrases.clear()


stt.start(phrase_parser)
