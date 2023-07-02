import os

from spotipy import SpotifyOAuth, Spotify


class SpotifyClient:
    def __init__(self):
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        scope = "user-modify-playback-state"

        self.spotify = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope
            )
        )

    def auth_callback(self):
        pass

    def get_song_by_name(self, song_name: str, artist_name: str) -> str:
        search_query = f"{artist_name} - {song_name}"

        results = self.spotify.search(q=search_query, type='track')
        track_id = results['tracks']['items'][0]['uri']

        return track_id

    def play_track(self, track_uri: str):
        self.spotify.start_playback(uris=[track_uri])
