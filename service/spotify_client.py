import spotipy
from flask import redirect
import time
import random
from urllib.request import urlopen
import base64
import datetime

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

def create_playlist(spotify, bfs_genres):
    description = "This playlist was created with these genres {}!".format(", ".join(bfs_genres), )
    created_playlist = spotify.user_playlist_create(spotify.me()["id"], name="Degrees of Music playlist 🤠", description=description)
    spotify.playlist_upload_cover_image(created_playlist["id"], base64_img())
    return created_playlist["id"]

def search_genre_data(spotify, genres, playlist_id):
    for index in range(0, len(genres), 5):
        song_list = set()
        for count in range(index, index + 5):
            time.sleep(5)
            playlists = spotify.search(type="playlist", q=genres[count], limit=3)
            for playlist in playlists["playlists"]["items"]:
                if playlist["owner"]["display_name"] == "The Sounds of Spotify":
                    tracks = spotify.playlist_tracks(playlist["id"], "items(track(id))", 25)["items"]
                    for track in random.sample(tracks, 15):
                        song_list.add("spotify:track:{}".format(track["track"]["id"]))
                    break
                elif "picked just for you" in playlist["description"] and playlist["owner"]["display_name"] == "Spotify":
                    tracks = spotify.playlist_tracks(playlist["id"], "items(track(id))", 25)["items"]
                    for track in random.sample(tracks, 15):
                        song_list.add("spotify:track:{}".format(track["track"]["id"]))
                    break
                else:
                    tracks = spotify.playlist_tracks(playlists["playlists"]["items"][0]["id"], "items(track(id))", 20)["items"]
                    if len(tracks) < 15:
                        for inner_index in range(len(tracks)):
                            song_list.add("spotify:track:{}".format(tracks[inner_index]["track"]["id"]))
                    else:
                        for track in random.sample(tracks, 15):
                            song_list.add("spotify:track:{}".format(track["track"]["id"]))
                    break

        song_list = list(song_list)
        random.shuffle(song_list)
        spotify.playlist_add_items(playlist_id, song_list)

def base64_img():
    URL = 'https://senior-pics.s3.amazonaws.com/cap.jpg'
    with urlopen(URL) as url:
        f = url.read()
        image = base64.b64encode(f).decode("ascii")
        return image