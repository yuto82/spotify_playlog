import requests
from config import Config

def get_recent_tracks(access_token=Config.ACCESS_TOKEN):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api.spotify.com/v1/me/player/recently-played?limit=50"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(data["items"])
