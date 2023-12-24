import os

import uvicorn
from dotenv import load_dotenv

from kira_client.api import app
from kira_client.services import ConfigService, LedStripService, LoggerService, MicrophoneService, \
    VoiceTriggerDetectorService

DefaultModel = "gpt-3.5-turbo-0613"


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=3000)


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

    logger_service.info("Application started")

    voice_trigger_detector_service.listen(handle_trigger)


def handle_trigger():
    pass


if __name__ == "__main__":
    load_dotenv()

    # api_thread = threading.Thread(target=run_api)
    # api_thread.start()

    main()
