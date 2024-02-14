import os
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
from dotenv import load_dotenv
from service.graph_client import bfs
from service.spotify_client import retrieve_user_data, retrieve_user_genres, spotify_manager, search_genre_data, create_playlist
import threading

app = Flask(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

Session(app)
load_dotenv()

@app.get("/")
def read_root():
    return "Hello, World!"

@app.get("/login")
def login():
    scope = "user-top-read"
    cache_handler = spotipy.cache_handler.CacheFileHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    
    # 2. if user has logged in, redirect and cache token
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/login')
    
    # 1. if user has not logged in yet
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return {"auth_url": auth_url, "redirect_url": ""}

    # 3. user has been authenticated and redirected to proper URL
    return "url"

@app.get("/user-data")
def user_data():
    spotify = spotify_manager(session)
    return retrieve_user_data(spotify)

@app.get("/search")
def search():
    depth = int(request.args.get('depth'))
    spotify = spotify_manager(session)

    def threaded_function(depth):
        genres = list(retrieve_user_genres(spotify))
        bfs_genres = bfs(genres, depth)
        print(bfs_genres)
        song_list = search_genre_data(spotify, bfs_genres)
        create_playlist(spotify, song_list, bfs_genres)
    
    thread = threading.Thread(target=threaded_function, kwargs={'depth': depth})
    thread.start()
    
    # based on depth and genres length, return estimated mins
    return "x mins"

if __name__ == "__main__":
    app.run(debug=True)