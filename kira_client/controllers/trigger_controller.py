import tempfile

from kira_client.services import ConfigService, LoggerService, MicrophoneService, OpenAIClient, \
    VoiceTriggerDetectorService


class TriggerController:
    def __init__(
        self,
        voice_trigger_detector_service: VoiceTriggerDetectorService,
        microphone_service: MicrophoneService,
        logger_service: LoggerService,
        config_service: ConfigService,
        openai_client: OpenAIClient,
    ):
        self.voice_trigger_detector_service = voice_trigger_detector_service
        self.microphone_service = microphone_service
        self.logger_service = logger_service
        self.config_service = config_service
        self.openai_client = openai_client

    def listen(self):
        self.voice_trigger_detector_service.listen(self.__handle_trigger)

    def __handle_trigger(self):
        duration = self.config_service.MICROPHONE_RECORDING_DURATION
        self.logger_service.info(f"Recording audio for {duration} seconds...")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            self.microphone_service.record_audio(
                temp_file,
                channels=self.config_service.MICROPHONE_CHANNELS,
                duration=duration,
            )
            self.logger_service.info(f"Audio saved to {temp_file.name}")

            self.logger_service.info("Transcribing audio...")
            transcription = self.openai_client.transcribe(temp_file.file)
            self.logger_service.info(f"Transcription: {transcription}")
