from google.cloud.speech_v1 import SpeechClient
from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import types
import pyaudio
import pathlib

from microphone_input import MicrophoneInput

class SpeechToTextClient:
    """
    A speech to text client that parses microphone input into text.
    """
    def __init__(self, credentials_path, language_code, phrase_hints=[]):
        """
        Args:
            credentials_path (str): The path to the service account private key json file.
            language_code (str): The language of the supplied audio as a BCP-47 language tag. Example: “en-US”.
            phrase_hints (str[]): https://cloud.google.com/speech-to-text/docs/basics#phrase-hints
        """
        self.language_code = language_code

        self.client = SpeechClient().from_service_account_json(credentials_path)
        self.speech_context = [types.SpeechContext(phrases=phrase_hints)]

        self._mic: MicrophoneInput = None

    def start(self, callback):
        """
        Args:
            callback (function): Function that is called when text is transcribed from speech
        """
        with MicrophoneInput() as mic:
            print("Starting SpeechToTextClient")
            self._mic = mic
            audio_generator = self._mic.generator()

            config = types.RecognitionConfig(
                    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=self._mic.RATE,
                    language_code=self.language_code,
                    use_enhanced=True,
                    speech_contexts=self.speech_context
            )

            streaming_config = types.StreamingRecognitionConfig(config=config,
                                                                interim_results=True)

            requests = (types.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
            responses = self.client.streaming_recognize(streaming_config, requests)

            for response in responses:
                if not response.results: # no results
                    continue

                # first result is best result
                result = response.results[0]
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript.strip()
                callback((transcript, result.is_final))

    def close(self):
        print("Stopping SpeechToTextClient")
        if self._mic is None or self._mic.closed:
            return

        self._mic.close()

    def restart(self):
        self.stop()
        self.start()

    def update_phrase_hints(self, phrase_hints):
        self.phrase_hints = phrase_hints


if __name__ == "__main__":
    import os
    import time

    cred_path = os.path.abspath("secret.json")

    def callback(text):
        print(text)

    client = SpeechToTextClient(cred_path, "en-US")
    client.start(callback)
    time.sleep(2)
    client.stop()
