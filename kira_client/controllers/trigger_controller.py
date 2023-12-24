import tempfile

from kira_client.services import ConfigService, LoggerService, MicrophoneService, VoiceTriggerDetectorService


class TriggerController:
    def __init__(
        self,
        voice_trigger_detector_service: VoiceTriggerDetectorService,
        microphone_service: MicrophoneService,
        loggger_service: LoggerService,
        config_service: ConfigService,
    ):
        self.voice_trigger_detector_service = voice_trigger_detector_service
        self.microphone_service = microphone_service
        self.loggger_service = loggger_service
        self.config_service = config_service

    def listen(self):
        self.voice_trigger_detector_service.listen(self.__handle_trigger)

    def __handle_trigger(self):
        duration = self.config_service.MICROPHONE_RECORDING_DURATION
        self.loggger_service.info(f"Recording audio for {duration} seconds...")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            self.microphone_service.record_audio(
                temp_file,
                channels=self.config_service.MICROPHONE_CHANNELS,
                duration=duration,
            )

            self.loggger_service.info(f"Audio saved to {temp_file.name}")
