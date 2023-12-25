from typing import Any

from httpx import Client


class HttpClient:
    @staticmethod
    def request(method: str, url: str) -> Any:
        with (Client() as client):
            resp = client.request(method, url)
            resp.raise_for_status()

            return resp.text
