import os
from types import SimpleNamespace

import requests

GENIUS_API_BASE_URL = "https://api.genius.com"


class GeniusTrack(SimpleNamespace):
    id: int
    artist_names: str
    title: str


class GeniusClient:
    def __init__(self):
        pass

    def search(self, search_query: str) -> GeniusTrack:
        params = {
            "q": search_query
        }
        headers = {
            "Authorization": f"Bearer {os.getenv('GENIUS_API_KEY')}",
        }

        resp = requests.get(f"{GENIUS_API_BASE_URL}/search", params=params, headers=headers)
        resp_body = resp.json()

        tracks = list(filter(lambda x: x["type"] == "song", resp_body["response"]["hits"]))
        most_relevant_track = tracks[0]["result"]
        most_relevant_track["title"] = self._remove_translated_name(most_relevant_track["title_with_featured"])

        return GeniusTrack(**most_relevant_track)

    @staticmethod
    def _remove_translated_name(track_name: str) -> str:
        last_opening_parenthesis_index = track_name.rfind('(')

        if last_opening_parenthesis_index != -1:
            cleaned_track_name = track_name[:last_opening_parenthesis_index].strip()
            return cleaned_track_name
        else:
            return track_name

