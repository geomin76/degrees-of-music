import spotipy
from flask import redirect

def spotify_manager(session):
    cache_handler = spotipy.cache_handler.CacheFileHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify

def retrieve_user_data(spotify):
    user_data = {
        "genres": [],
        "artist_data": []
    }
    genres = set()
    for index, artist_data in enumerate(spotify.current_user_top_artists(time_range="short_term", limit=5)['items']):
        genres.update(artist_data["genres"])
        artist_data_to_insert = {
            "index": index,
            "name": artist_data["name"],
            "image": artist_data["images"][0]["url"]
        }
        user_data["artist_data"].append(artist_data_to_insert)
    user_data["genres"] = list(genres)
    return user_data

def retrieve_user_genres(spotify):
    genres = set()
    for artist_data in spotify.current_user_top_artists(time_range="short_term", limit=5)['items']:
        genres.update(artist_data["genres"])
    return genres

def create_playlist(spotify, song_list, bfs_genres):
    # create playlist with songs provided
    # add genres to description
    # add songs to playlist!
    return ""

def search_genre_data(spotify, genres):
    # with time.sleep so no overload, but retrieve songs randomly from playlists from genres
    # and generate all songs and return
    return ""