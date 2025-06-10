import json
import requests
from pathlib import Path
from components.settings.config import Config
from components.access_token import refresh_access_token

def extract(client_id: str, client_secret: str):
    refreshed_access_token = refresh_access_token(client_id, client_secret)
    
    headers = {
        "Authorization": f"Bearer {refreshed_access_token}"
    }
    url = "https://api.spotify.com/v1/me/player/recently-played?limit=50"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    spotify_data = response.json()

    spotify_data_file = Path(__file__).parent.parent / "tmp" / "data" / "spotify_data.json"

    with open(spotify_data_file, "w") as file:
            json.dump(spotify_data, file, indent=4)

if __name__ == "__main__":
    extract(Config.CLIENT_ID,
            Config.CLIENT_SECRET)