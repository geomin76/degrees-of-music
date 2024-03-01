import os
from flask import Flask, session, request, redirect, render_template
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
def login():
    scope = "user-top-read playlist-read-private user-read-private user-read-email ugc-image-upload playlist-modify-public playlist-modify-private"
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
        return render_template("login.html", auth_url=auth_url)

    # 3. user has been authenticated and redirected to proper URL
    return redirect("/index")

@app.get("/index")
def index():
    spotify = spotify_manager(session)
    data = retrieve_user_data(spotify)

    return render_template("index.html", name=spotify.me()["display_name"], data=data)


@app.post("/search")
def search():
    depth = int(request.form['depth'])
    spotify = spotify_manager(session)
    
    def threaded_function(depth):
        genres = list(retrieve_user_genres(spotify))
        bfs_genres = bfs(genres, depth)
        playlist_id = create_playlist(spotify, bfs_genres)
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
    
    return render_template("submit.html", time=time)

if __name__ == "__main__":
    app.run(debug=True)