from typing import IO

from openai import OpenAI

from kira_client.services import ConfigService


class OpenAIClient:
    def __init__(self, config_service: ConfigService):
        self.client = OpenAI(api_key=config_service.OPENAI_API_KEY)
        self.config_service = config_service

    def transcribe(self, audio_file: IO[bytes]) -> str:
        resp = self.client.audio.transcriptions.create(
            model=self.config_service.OPENAI_SPEACH_RECOGNITION_MODEL,
            file=audio_file,
        )

        return resp.text
