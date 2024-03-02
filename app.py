import os
from flask import Flask, session, request, redirect, render_template
import spotipy
from dotenv import load_dotenv
from service.graph_client import bfs
from service.spotify_client import retrieve_user_data, retrieve_user_genres, search_genre_data, create_playlist
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

load_dotenv()

@app.get("/")
def main():
    cleanup()
    scope = "user-top-read playlist-read-private user-read-private user-read-email ugc-image-upload playlist-modify-public playlist-modify-private"
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                               show_dialog=True)
        
    # 2. if user has logged in, redirect and cache token
    if request.args.get("code"):
        cleanup()
        session['tokens'] = {
            'access_token': auth_manager.get_access_token(request.args.get("code"))["access_token"]
        }
        return redirect('/')
    
    # 1. if user has not logged in yet
    if 'tokens' not in session:
        cleanup()
        auth_url = auth_manager.get_authorize_url()
        return render_template("login.html", auth_url=auth_url)

    # 3. user has been authenticated and redirected to proper URL
    return redirect("/index")

@app.get("/index")
def index():
    cleanup()
    spotify = spotipy.Spotify(auth=session['tokens'].get('access_token'))
    data = retrieve_user_data(spotify)

    return render_template("index.html", name=spotify.me()["display_name"], data=data)


@app.post("/search")
def search():
    depth = int(request.form['depth'])
    cleanup()
    spotify = spotipy.Spotify(auth=session['tokens'].get('access_token'))
    
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

def cleanup():
    cache_file = '.cache'
    if os.path.exists(cache_file):
        os.remove(cache_file)


if __name__ == "__main__":
    app.run(debug=True)