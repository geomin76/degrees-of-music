import requests
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import json
load_dotenv()

data = {}
with open('./data.json') as f:
    data = json.load(f)

def get_token(token, time):
    if not token or (time - datetime.now()).seconds > 3600:
        print("Getting new token!")
        token_data = requests.post("https://accounts.spotify.com/api/token", headers={"Content-Type": "application/x-www-form-urlencoded"}, data={"grant_type": "client_credentials", "client_id": os.environ["CLIENT_ID"], "client_secret": os.environ["CLIENT_SECRET"]})
        token = token_data.json()["access_token"]
        return (token, datetime.now())
    return (token, time)

token = None
token_time = datetime.now()
# seed genres that Spotify uses for /recommendation endpoint

# 1/15/24 - Stopped after Dub. Run at Dubstep, starting at index 30
# 1/16/24 - Stopped during Gospel. starting at index 41
# 1/16/24 - Stopped during sleep
# 1/17/24 - Done
genres = ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", "bluegrass", "blues", "bossanova", "brazil", "breakbeat", "british", "cantopop", "chicago-house", "children", "chill", "classical", "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", "disco", "disney", "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "emo", "folk", "forro", "french", "funk", "garage", "german", "gospel", "goth", "grindcore", "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore", "hardstyle", "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop", "industrial", "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "latino", "malay", "mandopop", "metal", "metal-misc", "metalcore", "minimal-techno", "movies", "mpb", "new-age", "new-release", "opera", "pagode", "party", "philippines-opm", "piano", "pop", "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip", "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba", "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter", "soul", "soundtracks", "spanish", "study", "summer", "swedish", "synth-pop", "tango", "techno", "trance", "trip-hop", "turkish", "work-out", "world-music"]
try:
    for INDEX in range(len(genres)):
        token, token_time = get_token(token, token_time)
        print("Got token!")
        time.sleep(15)

        # get recommendations of genre, list out artists, then get designated genres of each artist with time in between
        recommendation_data = requests.get("https://api.spotify.com/v1/recommendations", headers={"Authorization": "Bearer " + token}, params={"seed_genres": genres[INDEX]})
        genres_set = set()
        for track in recommendation_data.json()["tracks"]:
            for artist in track["artists"]:
                time.sleep(15)
                print("Found artist {} for genre {}".format(artist["name"], genres[INDEX]))
                artist_data = requests.get("https://api.spotify.com/v1/artists/{}".format(artist["id"]), headers={"Authorization": "Bearer " + token})
                print("Retrieved artist data for artist {} with genres {}".format(artist["name"], str(artist_data.json()["genres"])))
                for genre in artist_data.json()["genres"]:
                    genres_set.add(genre)
        data[genres[INDEX]] = list(genres_set)

except Exception as e:
    print("Received error")
    print(e)
    with open('./data.json', 'w') as f:
        json.dump(data, f)

finally:
    with open('./data.json', 'w') as f:
        json.dump(data, f)