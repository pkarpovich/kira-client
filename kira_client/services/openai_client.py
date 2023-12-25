from typing import IO

from jinja2 import Template
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

    def text_completion(self, prompt: str, user_request: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.config_service.OPENAI_CHAT_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": user_request,
                }
            ]
        )

        return resp.choices[0].message.content

    @staticmethod
    def populate_template_with_variables(template: str, variables: dict) -> str:
        return Template(template).render(variables)
