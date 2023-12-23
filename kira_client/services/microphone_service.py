from pyaudio import paInt16, PyAudio, Stream


class MicrophoneService:
    def __init__(self):
        self.pa = PyAudio()

    def listen(self, frame_length: int, rate: int = 44100, channels: int = 1) -> Stream:
        return self.pa.open(
            frames_per_buffer=frame_length,
            channels=channels,
            format=paInt16,
            input=True,
            rate=rate,
        )
