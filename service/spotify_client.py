import requests
from dotenv import load_dotenv
from datetime import datetime

def get_token(token, time):
    if not token or (time - datetime.now()).seconds > 3600:
        print("Getting new token!")
        token_data = requests.post("https://accounts.spotify.com/api/token", headers={"Content-Type": "application/x-www-form-urlencoded"}, data={"grant_type": "client_credentials", "client_id": os.environ["CLIENT_ID"], "client_secret": os.environ["CLIENT_SECRET"]})
        token = token_data.json()["access_token"]
        return (token, datetime.now())
    return (token, time)