import json
import tempfile
from threading import Timer
from typing import IO

from kira_client.prompts import IntentRecognitionPrompt
from kira_client.services import Colors, ConfigService, IntentService, LedStripService, LoggerService, \
    MicrophoneService, OpenAIClient, \
    VoiceTriggerDetectorService


class TriggerController:
    def __init__(
        self,
        voice_trigger_detector_service: VoiceTriggerDetectorService,
        microphone_service: MicrophoneService,
        led_strip_service: LedStripService,
        logger_service: LoggerService,
        config_service: ConfigService,
        intent_service: IntentService,
        openai_client: OpenAIClient,
    ):
        self.voice_trigger_detector_service = voice_trigger_detector_service
        self.microphone_service = microphone_service
        self.led_strip_service = led_strip_service
        self.logger_service = logger_service
        self.config_service = config_service
        self.intent_service = intent_service
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
            self.led_strip_service.light_up(Colors.Yellow)

            transcription = self.__transcribe_audio(temp_file.file)
            self.led_strip_service.light_up(Colors.Orange)

            intent = self.__recognize_intent(transcription)
            self.led_strip_service.light_up(Colors.Purple)
            self.logger_service.info(f"Intent: {intent}")

            is_processed = self.intent_service.process_intent_action(intent)
            result_color = Colors.Green if is_processed else Colors.Red
            self.logger_service.info(f"Intent processed: {is_processed}")
            self.led_strip_service.light_up(result_color)

            Timer(3.0, self.led_strip_service.clear).start()

    def __transcribe_audio(self, temp_file: IO[bytes]) -> str:
        self.logger_service.info("Transcribing audio...")
        transcription = self.openai_client.transcribe(temp_file)
        self.logger_service.info(f"Transcription: {transcription}")

        return transcription

    def __recognize_intent(self, transcription: str) -> str:
        self.logger_service.info("Recognizing intent...")

        intents = self.intent_service.get_all_intents()
        prompt = self.openai_client.populate_template_with_variables(
            IntentRecognitionPrompt,
            {
                "intents": intents,
            }
        )
        intent_resp = self.openai_client.text_completion(prompt, transcription)
        return json.loads(intent_resp)["intent"]
