import sys
import pathlib
from argparse import ArgumentParser
from config import Config
from speech_to_text import SpeechToTextClient

parser = ArgumentParser()
parser.add_argument('-c', '--config', required=True)
args = parser.parse_args(sys.argv[1:])
cfg = Config(args.config)


def phrase_parser(phrase):
    print(phrase)


secret_path = pathlib.Path(__file__).parent.parent / 'secret.json'
stt = SpeechToTextClient(secret_path, 'en-US')
stt.start(phrase_parser)
