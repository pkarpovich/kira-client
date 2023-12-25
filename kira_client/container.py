import os

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from kira_client.controllers import TriggerController
from kira_client.services import ConfigService, LedStripService, LoggerService, MicrophoneService, \
    OpenAIClient, VoiceTriggerDetectorService
from kira_client.stores import IntentStore


class Container(DeclarativeContainer):
    logger_service = providers.Singleton(LoggerService)
    config_service = providers.Factory(ConfigService, env=os.environ)

    is_led_strip_enabled = providers.Callable(
        lambda config_service: config_service.LED_STRIP_ENABLED,
        config_service=config_service
    )

    intent_store_path = providers.Callable(
        lambda config_service: config_service.INTENT_STORE_PATH,
        config_service=config_service
    )

    intent_store = providers.Singleton(
        IntentStore,
        file_path=intent_store_path
    )

    microphone_service = providers.Singleton(MicrophoneService)
    led_strip_service = providers.Singleton(LedStripService, enabled=is_led_strip_enabled)
    voice_trigger_detector_service = providers.Singleton(
        VoiceTriggerDetectorService,
        microphone_service=microphone_service,
        led_strip_service=led_strip_service,
        config_service=config_service,
        logger_service=logger_service,
    )
    openai_client = providers.Factory(OpenAIClient, config_service=config_service)

    trigger_controller = providers.Singleton(
        TriggerController,
        voice_trigger_detector_service=voice_trigger_detector_service,
        microphone_service=microphone_service,
        logger_service=logger_service,
        config_service=config_service,
        openai_client=openai_client,
        intent_store=intent_store
    )
