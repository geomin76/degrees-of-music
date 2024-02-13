import os
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
from dotenv import load_dotenv

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
    scope = "user-library-read"
    cache_handler = spotipy.cache_handler.CacheFileHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private',
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    
    # 2. if user has logged in, redirect and cache token
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/login')
    
    # 1. if user has not logged in yet
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return auth_url

    # 3. user has been authenticated and redirected to proper URL
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return "url"

@app.get("/user-data")
def user_data():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    # add user data of top 5 artists with img, name, genres
    user_data = {}
    return "ok"

@app.get("/search")
def search():
    # get genres + depth of search (max 1-3 depths)
    # some kind of thread work like below, where it returns estimated time and starts bfs and does create playlist
    # in the playlist, put generic title and add in description what genres it picked

    """
    @app.route('/start_task')
    def start_task():
        def do_work(value):
            # do something that takes a long time
            import time
            time.sleep(value)

        thread = Thread(target=do_work, kwargs={'value': request.args.get('value', 20)})
        thread.start()
        return 'started'
    """
    return "ok"


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

if __name__ == "__main__":
    app.run(debug=True)