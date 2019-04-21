from google.cloud.speech_v1 import SpeechClient
from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import types
import pyaudio
import pathlib

from microphone_input import MicrophoneInput


class SpeechToText:
    def __init__(self, credentials_path, language_code):
        self.language_code = language_code
        self.client = SpeechClient().from_service_account_json(credentials_path)

    def start_listen(self, callback):
        with MicrophoneInput() as mic:
            audio_generator = mic.generator()

            config = types.RecognitionConfig(
                    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=mic.RATE,
                    language_code=language_code
            )

            streaming_config = types.StreamingRecognitionConfig(config=config)
                                                                # interim_results=True)

            requests = (types.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
            responses = self.client.streaming_recognize(streaming_config, requests)

            for response in responses:
                if not response.results: # no results
                    continue

                # first result is best result
                result = response.results[0]
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript
                callback(transcript)



