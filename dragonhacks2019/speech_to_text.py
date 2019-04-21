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
    def __init__(self, credentials_path, language_code):
        """
        Args:
            credentials_path (str): The path to the service account private key json file.
            language_code (str): The language of the supplied audio as a BCP-47 language tag. Example: “en-US”.
        """
        self.language_code = language_code
        self.client = SpeechClient().from_service_account_json(credentials_path)

    def start(self, callback):
        """
        Args:
            callback (function): Function that is called when text is transcribed from speech
        """
        with MicrophoneInput() as mic:
            audio_generator = mic.generator()

            config = types.RecognitionConfig(
                    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=mic.RATE,
                    language_code=self.language_code,
                    use_enhanced=True
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

                transcript = result.alternatives[0].transcript.strip()
                callback(transcript)


if __name__ == "__main__":
    cred_path = pathlib.Path(__file__).parent / \
                         'credentials/dragon_hacks_2019.json'

    def callback(text):
        print(text)

    client = SpeechToTextClient(cred_path, "en-US")
    client.start(callback)
