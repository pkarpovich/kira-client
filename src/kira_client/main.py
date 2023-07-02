import os
import threading

import uvicorn

from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI

from src.kira_client.api import app
from src.kira_client.genius_chain import GeniusChain
from src.kira_client.services.spotify_client import SpotifyClient

DefaultModel = "gpt-3.5-turbo-0613"


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=3000)


def main():
    if os.getenv("OPENAI_API_KEY") is None:
        raise ValueError("OPENAI_API_KEY is not set")

    spotify_client = SpotifyClient()

    model = os.getenv("OPENAI_MODEL") or DefaultModel

    llm = ChatOpenAI(temperature=0, model=model)

    text = "Они видят мою боль, но боятся подойти, а мне хочется всего лишь оказаться среди них"

    genius_chain = GeniusChain(llm)
    resp = genius_chain.run(text)
    print(resp)

    track_id = spotify_client.get_song_by_name(resp.song_name, resp.artist_name)
    spotify_client.play_track(track_id)


if __name__ == "__main__":
    load_dotenv()

    api_thread = threading.Thread(target=run_api)
    api_thread.start()

    main()
