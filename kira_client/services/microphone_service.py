import wave
from contextlib import contextmanager
from typing import IO

from pyaudio import paInt16, PyAudio, Stream


class MicrophoneService:
    def __init__(self):
        self.pa = PyAudio()

    @contextmanager
    def listen(self, frame_length: int, rate: int = 44100, channels: int = 1) -> Stream:
        stream = self.pa.open(
            frames_per_buffer=frame_length,
            channels=channels,
            format=paInt16,
            input=True,
            rate=rate,
        )

        try:
            yield stream
        finally:
            stream.stop_stream()
            stream.close()

    def record_audio(
        self,
        file: IO[bytes],
        duration: int = 5,
        rate: int = 44100,
        channels: int = 1,
        chunk_size: int = 1024
    ):
        with self.listen(frame_length=chunk_size, rate=rate, channels=channels) as stream:
            frames = [stream.read(chunk_size) for _ in range(int(rate / chunk_size * duration))]

            with wave.open(file, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(self.pa.get_sample_size(paInt16))
                wf.setframerate(rate)
                wf.writeframes(b''.join(frames))
