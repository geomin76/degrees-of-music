import os
import spotipy
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    scope = "user-library-read"
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private',
                                               show_dialog=True)
    
    auth_url = auth_manager.get_authorize_url()
    return auth_url

"""
FLOW:
- Hit Spotify API "authorize" route, and obtain URL and return to frontend

https://github.com/spotipy-dev/spotipy/blob/a14a28e10c1889cce83eec7a7e1ad4b5944a452d/examples/app.py#L39-L62

- Frontend does "window.replace" with that URL to get spotify auth
- After auth, redirect URL will go to backend and retrieve code and then will get access token, storing it in session
- User in frontend will hit the BFS depth and track vs artist (check on that)
- Then user will be informed that playlist is creating and will be done in x seconds/mins
- Backend does graph search and creates playlist
"""