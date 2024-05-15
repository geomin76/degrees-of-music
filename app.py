import os
from flask import Flask, session, request, redirect, render_template
import spotipy
from dotenv import load_dotenv
from service.graph_client import bfs
from service.spotify_client import retrieve_user_data, retrieve_user_genres, search_genre_data, create_playlist
import threading
from flask_session import Session
import uuid

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')


@app.get("/")
def main():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    scope = "user-top-read playlist-read-private user-read-private user-read-email ugc-image-upload playlist-modify-public playlist-modify-private"
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                               cache_path=session_cache_path(),
                                               show_dialog=True)
        
    # 2. if user has logged in, redirect and cache token
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')
    
    # 1. if user has not logged in yet
    if not auth_manager.get_cached_token():
        auth_url = auth_manager.get_authorize_url()
        return render_template("login.html", auth_url=auth_url)

    # 3. user has been authenticated and redirected to proper URL
    return redirect("/index")

@app.get("/index")
def index():
    # TODO: fix auth for user, copy the "spotify for you" route
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path=session_cache_path())   
    if not auth_manager.get_cached_token():
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    data = retrieve_user_data(spotify)

    return render_template("index.html", name=spotify.me()["display_name"], data=data)


@app.post("/search")
def search():
    depth = int(request.form['depth'])
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path=session_cache_path())
    if not auth_manager.get_cached_token():
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    
    def threaded_function(depth):
        genres = list(retrieve_user_genres(spotify))
        bfs_genres = bfs(genres, depth)
        playlist_id = create_playlist(spotify, bfs_genres)

        # TODO: build caching here for search genre data
        search_genre_data(spotify, bfs_genres, playlist_id)

    thread = threading.Thread(target=threaded_function, kwargs={'depth': depth})
    thread.start()
    time = ""
    if depth == 1:
        time = "1 - 2 minutes"
    elif depth == 2:
        time = "2 - 3 minutes"
    elif depth == 3: 
        time = "3 - 5 minutes"
    
    # TODO: perhaps instead of time, find the bfs data first and display the genres related and their "path of genres" to how it got there!
    return render_template("submit.html", time=time)

if __name__ == "__main__":
    app.run(debug=True)