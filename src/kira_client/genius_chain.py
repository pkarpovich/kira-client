import json
import os
from types import SimpleNamespace

from langchain.base_language import BaseLanguageModel

from genius_api_prompt import GENIUS_API_DOCS, GENIUS_API_RESPONSE_PROMPT
from langchain.chains import APIChain


class GeniusTrackResult(SimpleNamespace):
    track_id: int
    artist_name: str
    song_name: str


class GeniusChain:
    def __init__(self, llm: BaseLanguageModel, debug: bool = False):
        headers = {
            "Authorization": f"Bearer {os.getenv('GENIUS_API_KEY')}",
        }

        self.genius_chain = APIChain.from_llm_and_api_docs(
            llm,
            GENIUS_API_DOCS,
            api_response_prompt=GENIUS_API_RESPONSE_PROMPT,
            headers=headers,
            verbose=debug is True,
        )

    def run(self, search_query: str) -> GeniusTrackResult:
        response = self.genius_chain.run(search_query)

        return json.loads(response, object_hook=lambda d: GeniusTrackResult(**d))
