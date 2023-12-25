from struct import unpack_from

from pvporcupine import create
from pyaudio import Stream

from kira_client.services import Colors, ConfigService, LedStripService, LoggerService, MicrophoneService


class VoiceTriggerDetectorService:
    def __init__(
        self,
        config_service: ConfigService,
        logger_service: LoggerService,
        microphone_service: MicrophoneService,
        led_strip_service: LedStripService
    ):
        self.porcupine = create(
            keyword_paths=[config_service.PORCUPINE_MODEL_PATH],
            access_key=config_service.PORCUPINE_ACCESS_KEY,
        )
        self.microphone_service = microphone_service
        self.led_strip_service = led_strip_service
        self.logger_service = logger_service
        self.config_service = config_service

    def listen(self, trigger_cb: callable):
        try:
            while True:
                self.logger_service.info("Starting/Resuming voice detection...")

                with self.__create_audio_stream() as audio_stream:
                    while not self.__process_frame(audio_stream):
                        continue

                self.logger_service.info("Trigger word detected! Starting processing...")
                self.led_strip_service.light_up(Colors.Lavender)

                trigger_cb()

        except KeyboardInterrupt:
            self.logger_service.info("Stopping voice detection...")

        finally:
            self.porcupine.delete()
            self.logger_service.info("Voice detection stopped")

    def __create_audio_stream(self):
        return self.microphone_service.listen(
            frame_length=self.porcupine.frame_length,
            rate=self.porcupine.sample_rate,
            channels=ConfigService.MICROPHONE_CHANNELS,
        )

    def __process_frame(self, audio_stream: Stream) -> bool:
        pcm = audio_stream.read(self.porcupine.frame_length)
        pcm = unpack_from("h" * self.porcupine.frame_length, pcm)

        result = self.porcupine.process(pcm)

        return result != -1

    def __del__(self):
        if self.porcupine is None:
            return

        self.porcupine.delete()
