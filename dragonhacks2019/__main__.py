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


def phrase_parser(phrase):
    phrase, is_final = phrase
    print(phrase)
    for known_phrase in cfg.phrases():
        if known_phrase not in seen_phrases and known_phrase in phrase:
            seen_phrases.add(known_phrase)
            action.do_actions(*cfg.actions(known_phrase), cfg=cfg)
    if is_final:
        seen_phrases.clear()


secret_path = os.path.abspath('secret.json')
stt = SpeechToTextClient(secret_path, 'en-US', cfg.phrases())
stt.start(phrase_parser)
