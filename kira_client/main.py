import os
import threading

import uvicorn

from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI

from kira_client.api import app
from kira_client.genius_chain import GeniusChain
from kira_client.services import GeniusClient, SpotifyClient

DefaultModel = "gpt-3.5-turbo-0613"


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=3000)


def main():
    print('test')
    # if os.getenv("OPENAI_API_KEY") is None:
    #     raise ValueError("OPENAI_API_KEY is not set")
    #
    # genius_client = GeniusClient()
    # spotify_client = SpotifyClient()
    #
    # model = os.getenv("OPENAI_MODEL") or DefaultModel
    #
    # # llm = ChatOpenAI(temperature=0, model=model)
    #
    # text = "10age - пушка"
    # resp = genius_client.search(text)
    #
    # # genius_chain = GeniusChain(llm)
    # # resp = genius_chain.run(text)
    # # print(resp)
    # #
    #
    # track_id = spotify_client.get_song_by_name(resp.title, resp.artist_names)
    # spotify_client.play_track(track_id)


if __name__ == "__main__":
    load_dotenv()

    # api_thread = threading.Thread(target=run_api)
    # api_thread.start()

    main()
