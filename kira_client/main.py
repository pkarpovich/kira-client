import os

from dotenv import load_dotenv

from kira_client.controllers import TriggerController
from kira_client.services import (ConfigService, LedStripService, LoggerService, MicrophoneService, OpenAIClient,
                                  VoiceTriggerDetectorService)


def main():
    config_service = ConfigService(os.environ)
    logger_service = LoggerService()
    microphone_service = MicrophoneService()
    led_strip_service = LedStripService(config_service.LED_STRIP_ENABLED)
    voice_trigger_detector_service = VoiceTriggerDetectorService(
        config_service,
        logger_service,
        microphone_service,
        led_strip_service
    )
    openai_client = OpenAIClient(config_service)

    trigger_controller = TriggerController(
        voice_trigger_detector_service,
        microphone_service,
        logger_service,
        config_service,
        openai_client,
    )

    logger_service.info("Application started")
    trigger_controller.listen()


if __name__ == "__main__":
    load_dotenv()
    main()
