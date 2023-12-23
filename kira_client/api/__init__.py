from fastapi import FastAPI
from .spotify_api import spotify_router

app = FastAPI()

app.include_router(spotify_router)