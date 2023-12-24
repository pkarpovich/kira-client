from struct import unpack_from

from pvporcupine import create
from pyaudio import Stream

from kira_client.services import ConfigService, LoggerService, MicrophoneService


class VoiceTriggerDetectorService:
    def __init__(
        self,
        config_service: ConfigService,
        logger_service: LoggerService,
        microphone_service: MicrophoneService
    ):
        self.porcupine = create(
            keyword_paths=[config_service.PORCUPINE_MODEL_PATH],
            access_key=config_service.PORCUPINE_ACCESS_KEY,
        )
        self.microphone_service = microphone_service
        self.logger_service = logger_service

    def listen(self, trigger_cb: callable):
        audio_stream = self.microphone_service.listen(
            frame_length=self.porcupine.frame_length,
            rate=self.porcupine.sample_rate,
            channels=1,
        )

        try:
            self.logger_service.info("Starting voice detection...")
            while True:
                self.__process_frame(audio_stream, trigger_cb)

        except KeyboardInterrupt:
            self.logger_service.info("Stopping voice detection...")

        finally:
            audio_stream.close()
            self.porcupine.delete()
            self.logger_service.info("Voice detection stopped")

    def __process_frame(self, audio_stream: Stream, trigger_cb: callable):
        pcm = audio_stream.read(self.porcupine.frame_length)
        pcm = unpack_from("h" * self.porcupine.frame_length, pcm)

        result = self.porcupine.process(pcm)
        if result == -1:
            return

        self.logger_service.info("Trigger word detected!")
        trigger_cb()

    def __del__(self):
        if self.porcupine is None:
            return

        self.porcupine.delete()
