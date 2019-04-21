import pyaudio
import queue


class MicrophoneInput:
    """
    Helper class to put microphone input into a generator.
    """
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = int(self.RATE / 10)
        self._mic: pyaudio.PyAudio = None
        self._stream: pyaudio.Stream = None
        self._buf = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._mic = pyaudio.PyAudio()
        self._stream = self._mic.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK,
                                      stream_callback=self._fill_buf)
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self._stream.stop_stream()
        self._stream.close()
        self.closed = True
        self._buf.put(None)
        self._mic.terminate()


    def _fill_buf(self, in_data, frame_count, time_info, status_flags):
        self._buf.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """
        Returns: generator that gets filled with microphone data.
        """
        while not self.closed:
            # use blocking queue
            chunk = self._buf.get()
            # chunk is None if stream has ended
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self._buf.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)


if __name__ == '__main__':
    with MicrophoneInput() as mic:
        for chunk in mic.generator():
            print("Chunk")
            print(chunk)
